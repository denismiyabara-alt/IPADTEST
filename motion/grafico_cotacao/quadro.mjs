// Abre um projeto gerado num Chrome headless, posiciona a timeline no instante pedido e
// devolve, em JSON, o que está na tela (número, título, fonte) e os erros de JS da página.
// Uso: node grafico_cotacao/quadro.mjs <pasta-do-projeto> <segundos> [saida.png]
// Navegador: $PRODUCER_HEADLESS_SHELL_PATH, senão o do `npx hyperframes browser path`.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');
const [pasta, seg, png] = process.argv.slice(2);
const motion = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const raiz = path.resolve(pasta);

function navegador() {
  if (process.env.PRODUCER_HEADLESS_SHELL_PATH) return process.env.PRODUCER_HEADLESS_SHELL_PATH;
  const bin = path.join(motion, 'node_modules', '.bin', 'hyperframes');
  return execFileSync(bin, ['browser', 'path'], { encoding: 'utf8' }).trim().split('\n').pop();
}

const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2', '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav', '.json': 'application/json' };
const servidor = http.createServer((req, res) => {
  const f = path.join(raiz, decodeURIComponent(req.url.split('?')[0]).replace(/^\/$/, '/index.html'));
  if (!f.startsWith(raiz) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => servidor.listen(0, '127.0.0.1', r));
const { port } = servidor.address();
const b = await puppeteer.launch({ executablePath: navegador(), headless: true, args: ['--no-sandbox'] });
const erros = [];
try {
  const p = await b.newPage();
  p.on('pageerror', e => erros.push(String(e)));
  p.on('console', m => { if (m.type() === 'error') erros.push(m.text()); });
  p.on('requestfailed', r => erros.push('falhou: ' + r.url()));
  const raizEl = fs.readFileSync(path.join(raiz, 'index.html'), 'utf8').match(/data-width="(\d+)" data-height="(\d+)"/);
  await p.setViewport({ width: +raizEl[1], height: +raizEl[2] });
  await p.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate((t) => {
    const tl = window.__timelines && window.__timelines.grafico;
    if (!tl) return { erro: 'timeline "grafico" não registrada' };
    tl.seek(t, false);
    const txt = id => document.getElementById(id).textContent;
    const fontes = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
    const cs = (sel, prop) => { const e = document.querySelector(sel); return e ? getComputedStyle(e)[prop] : null; };
    const visivel = sel => { const e = document.querySelector(sel); if (!e) return false;
      const r = e.getBoundingClientRect(); let o = 1;
      for (let n = e; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity;
      return o > 0.9 && r.width > 0 && r.right <= innerWidth && r.bottom <= innerHeight; };
    const ressalva = document.getElementById('ressalva');
    return { t, duracao: tl.duration(), numero: txt('numero'), titulo: txt('titulo'), fonte: txt('fonte'),
             variacao: txt('variacao'), fontes,
             ressalva: ressalva ? ressalva.textContent : null, ressalvaVisivel: visivel('#ressalva'),
             cores: { fundo: cs('#root', 'backgroundColor'), numero: cs('#numero', 'color'),
                      linha: cs('#linha', 'stroke'), comp: cs('#linha-comp', 'stroke'), fonte: cs('#fonte', 'color') },
             familias: { numero: cs('#numero', 'fontFamily'), titulo: cs('#titulo', 'fontFamily') } };
  }, Number(seg));
  if (png) await p.screenshot({ path: png });
  console.log(JSON.stringify({ ...r, erros }));
} finally {
  await b.close();
  servidor.close();
}
