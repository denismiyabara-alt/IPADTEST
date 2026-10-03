// ponytail: print recortado de trecho de pagina via CDP (derivado de MORGAN STANLEY/cdp_shot.mjs)
// uso: node shot.mjs jobs.json   (lista de {id,url,anchor,grifo,end?,pad?,wait?,css?,vw?,probe?})
import { spawn } from "node:child_process";
import { writeFileSync, readFileSync } from "node:fs";
const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const OUT = "/Users/denal/Downloads/trxf11-cotista-recusou/prints";
const CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36";
const port = 9345;
const chrome = spawn(CH, ["--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=/tmp/chrome-cdp-trxf-cota",
  `--user-agent=${UA}`, "--window-size=1280,900", `--remote-debugging-port=${port}`, "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
await sleep(6000);
const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const ws = new WebSocket(targets.find(t => t.type === "page").webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = {};
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send("Page.enable"); await send("Runtime.enable");
const evalv = async (expression) => (await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result?.result?.value;

for (const j of jobs) {
  const vw = j.vw || 1280;
  await send("Emulation.setDeviceMetricsOverride", { width: vw, height: 900, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url: j.url });
  await sleep(j.wait || 9000);
  if (j.js) { await evalv(j.js); await sleep(3000); } // ex: clicar "Show All" antes de medir
  if (j.probe) { console.log(j.id, "PROBE", await evalv(`(() => { const t = document.body.innerText; const i = Math.max(0, t.indexOf(${JSON.stringify(j.ctx || "")}) - 300);
    return document.title + " || " + t.slice(i, i + ${j.probe}); })()`)); continue; }
  // esconde fixed/sticky (banner de cookie, paywall, header grudado) + css extra
  await evalv(`(() => { for (const el of document.querySelectorAll("body *")) { const p = getComputedStyle(el).position;
      if (p === "fixed" || p === "sticky") el.style.setProperty("display", "none", "important"); }
    document.documentElement.style.overflow = "visible"; document.body.style.overflow = "visible";
    // sem scrollbar: senao o captureBeyondViewport tira a barra e o layout anda ~8px depois de medido
    document.documentElement.style.setProperty("scrollbar-width", "none", "important");
    const s = document.createElement("style"); s.textContent = ${JSON.stringify(j.css || "")}; document.head.appendChild(s); })()`);
  const js = `(() => {
    const find = (needle) => { if (!needle) return null;
      // texto corrido de todos os nos visiveis, espacos colapsados, com mapa char -> (no, offset): acha trecho que cruza <strong> etc.
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, flat = "", map = [];
      while ((n = w.nextNode())) { if (!n.parentElement.getClientRects().length) continue;
        const t = n.textContent; for (let p = 0; p < t.length; p++) { const c = /\\s/.test(t[p]) ? " " : t[p];
          if (c === " " && flat.endsWith(" ")) continue; flat += c; map.push([n, p]); } }
      let i = -1, from = 0;
      while ((i = flat.indexOf(needle, from)) >= 0) { from = i + 1;
          const [n0, o0] = map[i], [n1, o1] = map[i + needle.length - 1];
          const r = document.createRange(); r.setStart(n0, o0); r.setEnd(n1, o1 + 1);
          if (!r.getBoundingClientRect().width) continue;
          let blk = r.commonAncestorContainer; if (blk.nodeType === 3) blk = blk.parentElement;
          while (blk && getComputedStyle(blk).display === "inline") blk = blk.parentElement;
          if (blk.getBoundingClientRect().width < 20) continue; // x.com: copia 1x1 escondida (leitor de tela) casa antes do post
          const ls = [...r.getClientRects()].filter(q => q.width > 1).map(q => [q.left + scrollX, q.top + scrollY, q.right + scrollX, q.bottom + scrollY]);
          const a = r.getBoundingClientRect(), b = blk.getBoundingClientRect(), sy = scrollY, sx = scrollX;
          return { ls, r: [a.left + sx, a.top + sy, a.right + sx, a.bottom + sy], b: [b.left + sx, b.top + sy, b.right + sx, b.bottom + sy] }; }
      return null; };
    return JSON.stringify({ a: find(${JSON.stringify(j.anchor)}), g: find(${JSON.stringify(j.grifo)}), e: find(${JSON.stringify(j.end || null)}) }); })()`;
  const f = JSON.parse(await evalv(js));
  if (!f.a || !f.g) { console.log(j.id, "NAO ACHOU", JSON.stringify(f)); continue; }
  const boxes = [f.a.b, f.g.b, f.e?.b].filter(Boolean), pad = j.pad ?? 30;
  let x0 = Math.max(0, Math.min(...boxes.map(b => b[0])) - pad), x1 = Math.max(...boxes.map(b => b[2])) + pad;
  if (j.x) [x0, x1] = j.x;
  const y0 = Math.max(0, Math.min(...boxes.map(b => b[1])) - pad), y1 = Math.max(...boxes.map(b => b[3])) + pad;
  const W = x1 - x0, H = y1 - y0, scale = Math.min(2.5, 1400 / W);
  const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: x0, y: y0, width: W, height: H, scale } });
  writeFileSync(`${OUT}/${j.id}.png`, Buffer.from(shot.result.data, "base64"));
  const g = f.g.r, fr = [(g[0] - x0) / W, (g[1] - y0) / H, (g[2] - x0) / W, (g[3] - y0) / H].map(v => +v.toFixed(4));
  // uma caixa por linha (mescla rects da mesma linha)
  const lin = []; for (const q of f.g.ls) { const l = lin.find(z => Math.abs(z[1] - q[1]) < 4); if (l) { l[0] = Math.min(l[0], q[0]); l[2] = Math.max(l[2], q[2]); l[3] = Math.max(l[3], q[3]); } else lin.push([...q]); }
  const linhas = lin.map(q => [(q[0] - x0) / W, (q[1] - y0) / H, (q[2] - x0) / W, (q[3] - y0) / H].map(v => +v.toFixed(4)));
  console.log(JSON.stringify({ id: j.id, bbox: fr, linhas, w: Math.round(W * scale), h: Math.round(H * scale) }));
}
ws.close(); chrome.kill();
