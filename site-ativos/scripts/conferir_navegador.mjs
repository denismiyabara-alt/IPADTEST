// Abre páginas geradas no Chromium headless, procura erros de JS e tira prints pequenas.
// Uso: node scripts/conferir_navegador.mjs   (com `python3 -m http.server 8765 -d saida` rodando)
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
// PLAYWRIGHT=caminho do pacote, se ele estiver instalado globalmente (ex.: $(npm root -g)/playwright)
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");
import { mkdirSync } from "node:fs";

const BASE = process.env.BASE || "http://127.0.0.1:8765";
const OUT = process.env.PRINTS || "prints";
mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const erros = [];
async function abrir(caminho, nome, acoes) {
  for (const [w, h, suf] of [[1000, 900, "desktop"], [390, 844, "celular"]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    page.on("pageerror", (e) => erros.push(`${caminho} [${suf}]: ${e.message}`));
    page.on("console", (m) => { if (m.type() === "error" && !/fonts\.g/.test(m.text() + (m.location().url || ""))) erros.push(`${caminho} [${suf}] console: ${m.text()}`); });
    await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
    await page.goto(BASE + caminho, { waitUntil: "load" });
    const largura = await page.evaluate(() => document.documentElement.scrollWidth);
    if (largura > w + 1) erros.push(`${caminho} [${suf}]: rolagem horizontal (${largura}px)`);
    await page.screenshot({ path: `${OUT}/${nome}-${suf}.jpg`, type: "jpeg", quality: 55 });
    if (acoes && suf === "desktop") await acoes(page, nome);
    await page.close();
  }
}
await abrir("/acoes/petr4/", "petr4", async (page, nome) => {
  const antes = await page.textContent("#g-bazin");
  await page.click("#g-calcular");
  const depois = await page.textContent("#g-bazin");
  console.log(`preco-justo PETR4: antes do clique "${antes}", depois "${depois}"`);
  if (antes.trim() !== "—" || depois.trim() === "—") erros.push("preco-justo não respeitou o cálculo só no clique");
  await page.locator("#preco-justo").screenshot({ path: `${OUT}/${nome}-preco-justo.jpg`, type: "jpeg", quality: 55 });
});
await abrir("/acoes/itub4/", "itub4");
await abrir("/fiis/hglg11/", "hglg11", async (page, nome) => {
  const v = await page.inputValue("#f-dy");
  console.log(`renda-fii HGLG11: f-dy preenchido com ${v}`);
  await page.locator("#renda-fii").screenshot({ path: `${OUT}/${nome}-renda-fii.jpg`, type: "jpeg", quality: 55 });
});
await abrir("/comparar/acoes/", "comparar", async (page) => {
  const linhas = await page.locator("#cmp-tabela tbody tr").count();
  console.log(`comparador: ${linhas} linhas`);
  if (linhas < 5) erros.push("comparador sem tabela");
});
await browser.close();
console.log(erros.length ? "ERROS:\n" + erros.join("\n") : "sem erros de JS");
process.exit(erros.length ? 1 : 0);
