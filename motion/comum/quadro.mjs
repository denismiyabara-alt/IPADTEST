// Abre um projeto HyperFrames num Chrome headless, posiciona a timeline em cada instante pedido e
// devolve, em JSON, o que a página diz que está na tela (window.__tela()) e os erros de JS/rede.
// Genérico: serve a qualquer peça da biblioteca que registre window.__timelines[<id>] e window.__tela.
// Uso: node comum/quadro.mjs <pasta-do-projeto> <seg>[,<seg>...] [prefixo-png]
//   (com prefixo, salva <prefixo>-<seg>.png de cada instante)
// Navegador: $PRODUCER_HEADLESS_SHELL_PATH, senão o do `npx hyperframes browser path`.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const motion = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const require = createRequire(path.join(motion, 'package.json'));
const puppeteer = require('puppeteer-core');
const [pasta, segs, png] = process.argv.slice(2);
const raiz = path.resolve(pasta);
const instantes = String(segs).split(',').map(Number);

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
  const html = fs.readFileSync(path.join(raiz, 'index.html'), 'utf8');
  const dim = html.match(/data-width="(\d+)" data-height="(\d+)"/);
  const comp = html.match(/data-composition-id="([^"]+)"/)[1];
  await p.setViewport({ width: +dim[1], height: +dim[2] });
  await p.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.fonts.ready);
  const quadros = [];
  for (const t of instantes) {
    const r = await p.evaluate((t, comp) => {
      const tl = window.__timelines && window.__timelines[comp];
      if (!tl) return { erro: `timeline "${comp}" não registrada` };
      tl.seek(t, false);
      return { t, duracao: tl.duration(), tela: window.__tela() };
    }, t, comp);
    if (png) await p.screenshot({ path: `${png}-${t}.png` });
    quadros.push(r);
  }
  const fontes = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '') + ' ' + f.weight));
  console.log(JSON.stringify({ quadros, fontes, erros }));
} finally {
  await b.close();
  servidor.close();
}
