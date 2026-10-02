// Teste de navegador das ferramentas: abre cada uma no Chromium headless, digita valores,
// confere os resultados, procura erros de JS e rolagem horizontal, e tira prints pequenas.
// As páginas são montadas pelo próprio plugin (tests/pagina.php imita o WordPress), servidas
// por um servidor HTTP embutido neste arquivo.
// Uso: PLAYWRIGHT=$(npm root -g)/playwright node tests/navegador.mjs
//      (CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome, se precisar)
import { createRequire } from "node:module";
import { createServer } from "node:http";
import { execFileSync } from "node:child_process";
import { readFileSync, mkdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = process.env.PRINTS || path.join(RAIZ, "prints", "1.3.0");
mkdirSync(OUT, { recursive: true });

const ANTIGAS = ["simulador-ntnb", "renda-fii", "lci-lca-cdb", "juros-anual-mensal", "renda-fixa-comparador", "perfil-investidor", "preco-justo"];
const NOVAS = ["um-milhao", "jcp-liquido", "aposentadoria-renda", "ir-fii-venda"];
const PAGINAS = {};
for (const id of [...ANTIGAS, ...NOVAS]) {
  PAGINAS[`/p/${id}`] = [`[iec_ferramenta id="${id}"]`];
  PAGINAS[`/p/${id}-compacto`] = [`[iec_ferramenta id="${id}" modo="compacto" metodologia="/metodologia/"]`];
}
PAGINAS["/p/um-milhao-preenchido"] = ['[iec_ferramenta id="um-milhao" um-aporte="2000" um-taxa="5" um-meta="500000" modo="compacto"]'];
PAGINAS["/p/renda-fii-preenchido"] = ['[iec_ferramenta id="renda-fii" f-dy="1,10" f-aporte="nada"]'];
PAGINAS["/p/jcp-liquido-data"] = ['[iec_ferramenta id="jcp-liquido" jcp-data="2025-12-15"]'];

const TIPOS = { ".css": "text/css", ".js": "text/javascript", ".html": "text/html" };
const servidor = createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  if (PAGINAS[url]) {
    const html = execFileSync("php", [path.join(RAIZ, "tests", "pagina.php"), "/iec-ferramentas", ...PAGINAS[url]]);
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); return res.end(html);
  }
  const arq = path.join(RAIZ, path.normalize(url));
  if (arq.startsWith(path.join(RAIZ, "iec-ferramentas")) && existsSync(arq)) {
    res.writeHead(200, { "content-type": (TIPOS[path.extname(arq)] || "application/octet-stream") + "; charset=utf-8" });
    return res.end(readFileSync(arq));
  }
  res.writeHead(404); res.end("não achei");
});
await new Promise((ok) => servidor.listen(0, "127.0.0.1", ok));
const BASE = `http://127.0.0.1:${servidor.address().port}`;

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const erros = [];
let conferidos = 0;
const txt = (s) => (s || "").replace(/ /g, " ").trim();

async function abrir(caminho, w, h) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  page.on("pageerror", (e) => erros.push(`${caminho} [${w}px]: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error" && !/fonts\.g/.test(m.text() + (m.location().url || ""))) erros.push(`${caminho} [${w}px] console: ${m.text()}`); });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  await page.goto(BASE + caminho, { waitUntil: "load" });
  const largura = await page.evaluate(() => document.documentElement.scrollWidth);
  if (largura > w + 1) erros.push(`${caminho} [${w}px]: rolagem horizontal (${largura}px)`);
  return page;
}
async function confere(page, sel, esperado, rotulo) {
  const v = txt(await page.textContent(sel));
  const ok = esperado instanceof RegExp ? esperado.test(v) : v === esperado;
  conferidos++;
  console.log(`${ok ? "ok  " : "ERRO"} ${rotulo}: ${sel} = "${v}"`);
  if (!ok) erros.push(`${rotulo}: ${sel} = "${v}", esperado ${esperado}`);
}
async function digita(page, sel, valor) { await page.fill(sel, String(valor)); }

// 1) Todas as ferramentas, normal e compacta, no desktop e no celular: sem erro de JS e sem rolagem lateral
for (const id of [...ANTIGAS, ...NOVAS]) {
  for (const suf of ["", "-compacto"]) {
    for (const [w, h] of [[1000, 900], [390, 844]]) {
      const page = await abrir(`/p/${id}${suf}`, w, h);
      if (suf) {
        const n = await page.locator("section.explain").count(), c = await page.locator(".iec-compacto a[href='/metodologia/']").count();
        if (n !== 0 || c !== 1) erros.push(`${id} compacto: explain=${n}, link=${c}`);
        if ((await page.getAttribute(".iec-ferramenta", "data-modo")) !== "compacto") erros.push(`${id} compacto sem data-modo`);
      }
      await page.close();
    }
  }
}

// 2) Conferências numéricas das ferramentas novas
{
  const p = await abrir("/p/um-milhao", 1000, 900);
  await confere(p, "#um-tempo", "30 anos e 5 meses", "um-milhao R$ 1.000/mês, 6% real, de zero até R$ 1 mi");
  await confere(p, "#um-tempo-nota", /365 meses/, "um-milhao meses");
  await digita(p, "#um-anos", 22);
  await confere(p, "#um-inv", "R$ 1.869,59", "um-milhao inverso, R$ 1 mi em 22 anos");
  await digita(p, "#um-meta", 534876);
  await confere(p, "#um-tempo", "22 anos", "um-milhao R$ 1.000/mês por 22 anos ≈ R$ 535 mil");
  await digita(p, "#um-meta", 1000000);
  if ((await p.locator("#um-tabela tr").count()) !== 31) erros.push("um-milhao: tabela deveria ter 31 anos");
  await p.click(".cenarios button[data-taxa='3']");
  if ((await p.inputValue("#um-taxa")) !== "3") erros.push("um-milhao: botão de cenário não trocou a taxa");
  await digita(p, "#um-taxa", 6);
  await p.screenshot({ path: `${OUT}/um-milhao-desktop.jpg`, type: "jpeg", quality: 50 });
  await p.close();
}
{
  const p = await abrir("/p/um-milhao-preenchido", 1000, 900);
  if ((await p.inputValue("#um-aporte")) !== "2000") erros.push("um-milhao preenchido: aporte não veio do shortcode");
  await confere(p, "#um-label", /R\$ 500\.000 guardando R\$ 2\.000,00 por mês, a 5% ao ano/, "um-milhao preenchido pelo shortcode");
  await p.screenshot({ path: `${OUT}/um-milhao-compacto.jpg`, type: "jpeg", quality: 50 });
  await p.close();
}
{
  const p = await abrir("/p/jcp-liquido", 1000, 900);
  await digita(p, "#jcp-por-acao", "1"); await digita(p, "#jcp-qtd", "1"); await digita(p, "#jcp-data", "2026-03-10");
  await confere(p, "#jcp-liq-acao", /R\$ 0,825 líquidos por ação, para R\$ 1,00 brutos/, "jcp R$ 1,00 em 2026");
  await confere(p, "#jcp-ir-k", "IR retido (17,5%)", "jcp alíquota 2026");
  await digita(p, "#jcp-data", "2025-12-15");
  await confere(p, "#jcp-liq-acao", /R\$ 0,85 líquidos/, "jcp R$ 1,00 em 2025");
  await digita(p, "#jcp-data", "2026-10-02"); await digita(p, "#jcp-qtd", "1000");
  await confere(p, "#jcp-liq", "R$ 825,00", "jcp R$ 1,00 × 1.000 ações");
  await confere(p, "#jcp-div", "R$ 1.000,00", "jcp dividendo igual, isento");
  await p.screenshot({ path: `${OUT}/jcp-liquido-desktop.jpg`, type: "jpeg", quality: 50 });
  await p.check("input[name='jcp-forma'][value='total']");
  await digita(p, "#jcp-total", "60000");
  await confere(p, "#jcp-liq", "R$ 49.500,00", "jcp total R$ 60 mil");
  await confere(p, "#jcp-div", "R$ 54.000,00", "jcp dividendo de R$ 60 mil no mês (10% retidos)");
  await p.close();
  const q = await abrir("/p/jcp-liquido-data", 390, 844);
  await confere(q, "#jcp-ir-k", "IR retido (15%)", "jcp data preenchida pelo shortcode (2025)");
  await q.close();
}
{
  const p = await abrir("/p/aposentadoria-renda", 1000, 900);
  await confere(p, "#ap-necessario", "R$ 1.800.000", "aposentadoria R$ 6.000/mês, retirada 4%");
  await digita(p, "#ap-inss", 2000);
  await confere(p, "#ap-necessario", "R$ 1.200.000", "aposentadoria com R$ 2.000 de INSS");
  if (await p.isVisible("#ap-aviso")) erros.push("aposentadoria: aviso de teto apareceu sem motivo");
  await digita(p, "#ap-inss", 9000);
  if (!(await p.isVisible("#ap-aviso"))) erros.push("aposentadoria: aviso de teto não apareceu");
  await digita(p, "#ap-inss", 0);
  await digita(p, "#ap-retirada", 3);
  await confere(p, "#ap-necessario", "R$ 2.400.000", "aposentadoria retirada 3%");
  await digita(p, "#ap-retirada", 4);
  await p.screenshot({ path: `${OUT}/aposentadoria-renda-desktop.jpg`, type: "jpeg", quality: 50 });
  await digita(p, "#ap-alvo", 30);
  await confere(p, "#ap-err", /maior que a sua idade/, "aposentadoria valida idades");
  await p.close();
}
{
  const p = await abrir("/p/ir-fii-venda", 1000, 900);
  await digita(p, "#fv-pm", 100); await digita(p, "#fv-venda", 110); await digita(p, "#fv-qtd", 100); await digita(p, "#fv-custos", 0);
  await digita(p, "#fv-data", "2026-10-02");
  await confere(p, "#fv-lucro", "R$ 1.000,00", "ir-fii lucro 100 cotas de R$ 100 a R$ 110");
  await confere(p, "#fv-ir", "R$ 200,00", "ir-fii IR 20%");
  await confere(p, "#fv-darf", "R$ 200,00", "ir-fii DARF");
  await confere(p, "#fv-venc", /30\/11\/2026/, "ir-fii vencimento");
  await p.screenshot({ path: `${OUT}/ir-fii-venda-desktop.jpg`, type: "jpeg", quality: 50 });
  await digita(p, "#fv-prejuizo", 300);
  await confere(p, "#fv-ir", "R$ 140,00", "ir-fii com R$ 300 de prejuízo anterior");
  await digita(p, "#fv-venda", 90);
  await confere(p, "#fv-darf", "R$ 0,00", "ir-fii venda com prejuízo");
  await confere(p, "#fv-resto", "R$ 1.300,00", "ir-fii prejuízo acumulado");
  await p.close();
}
{
  const p = await abrir("/p/renda-fii-preenchido", 390, 844);
  if ((await p.inputValue("#f-dy")) !== "1.10") erros.push("renda-fii: f-dy não veio do shortcode");
  if ((await p.inputValue("#f-aporte")) !== "500") erros.push("renda-fii: valor não numérico deveria ser ignorado");
  await p.close();
}

// 3) Prints no celular (390 px)
for (const id of NOVAS) {
  const p = await abrir(`/p/${id}`, 390, 844);
  await p.locator(`#${id} > .grid`).screenshot({ path: `${OUT}/${id}-celular.jpg`, type: "jpeg", quality: 45 });
  await p.close();
}

await browser.close();
servidor.close();
console.log(`${conferidos} conferências de valor`);
console.log(erros.length ? "ERROS:\n" + erros.join("\n") : "sem erros de JS, sem rolagem horizontal, valores conferidos");
process.exit(erros.length ? 1 : 0);
