/* Testes dos cálculos das ferramentas 1.3.0. Sem dependências: node --test tests/ */
"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const F = (id) => require(path.join(__dirname, "..", "iec-ferramentas", "ferramentas", id, "app.js"));

const perto = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg || ""} esperado ${b}, veio ${a}`);

test("um-milhao: taxa mensal equivalente de 6% ao ano", () => {
  const c = F("um-milhao");
  perto(c.taxaMensal(0.06), 0.0048675506, 1e-9);
  perto(Math.pow(1 + c.taxaMensal(0.06), 12), 1.06, 1e-12);
});

test("um-milhao: R$ 1.000/mês a 6% real, partindo de zero, chega a R$ 1 milhão em 365 meses (30 anos e 5 meses)", () => {
  const c = F("um-milhao");
  assert.equal(c.mesesAteMeta(0, 1000, 0.06, 1e6), 365);
  assert.ok(c.saldoFinal(0, 1000, 0.06, 364) < 1e6);
  assert.ok(c.saldoFinal(0, 1000, 0.06, 365) >= 1e6);
  perto(c.saldoFinal(0, 1000, 0.06, 365), 1003511.36, 0.01);
});

test("um-milhao: R$ 1.000/mês por 22 anos a 6% real ≈ R$ 535 mil", () => {
  const c = F("um-milhao");
  perto(c.saldoFinal(0, 1000, 0.06, 264), 534876.30, 0.01);
  perto(c.serie(0, 1000, 0.06, 264)[264], c.saldoFinal(0, 1000, 0.06, 264), 1e-6, "série e fórmula fechada");
});

test("um-milhao: inverso devolve o aporte que fecha a meta", () => {
  const c = F("um-milhao");
  const pmt = c.aporteNecessario(0, 1e6, 0.06, 22 * 12);
  perto(pmt, 1869.59, 0.01);
  perto(c.saldoFinal(0, pmt, 0.06, 264), 1e6, 1e-6);
  assert.equal(c.aporteNecessario(2e6, 1e6, 0.06, 12), 0, "inicial já passa da meta");
  perto(c.aporteNecessario(0, 120000, 0, 120), 1000, 1e-9, "taxa zero");
  assert.equal(c.mesesAteMeta(0, 0, 0, 1), null);
});

test("jcp-liquido: R$ 1,00 de JCP vira R$ 0,825 em 2026 e R$ 0,85 antes", () => {
  const c = F("jcp-liquido");
  perto(c.jcp(1, "2026-03-10").liquido, 0.825, 1e-12);
  perto(c.jcp(1, "2026-01-01").liquido, 0.825, 1e-12);
  perto(c.jcp(1, "2025-12-31").liquido, 0.85, 1e-12);
  perto(c.jcp(100, "2026-10-02").ir, 17.5, 1e-9);
});

test("jcp-liquido: dividendo isento até R$ 50 mil no mês; acima, 10% sobre o total (2026+)", () => {
  const c = F("jcp-liquido");
  assert.equal(c.dividendo(50000, "2026-05-01").ir, 0);
  perto(c.dividendo(50000.01, "2026-05-01").ir, 5000.001, 1e-6);
  perto(c.dividendo(60000, "2026-05-01").liquido, 54000, 1e-9);
  assert.equal(c.dividendo(60000, "2025-11-30").ir, 0, "antes de 2026, isento");
});

test("aposentadoria-renda: patrimônio necessário pela regra de retirada", () => {
  const c = F("aposentadoria-renda");
  perto(c.patrimonioNecessario(6000, 0, 0.04), 1.8e6, 1e-6);
  perto(c.patrimonioNecessario(6000, 2000, 0.04), 1.2e6, 1e-6);
  assert.equal(c.patrimonioNecessario(3000, 4000, 0.04), 0);
  assert.equal(c.TETO_INSS_2026, 8475.55);
});

test("aposentadoria-renda: simulação completa fecha com o aporte necessário", () => {
  const c = F("aposentadoria-renda");
  const p = { idade: 35, alvo: 60, renda: 6000, inss: 0, patrimonio: 50000, aporte: 1500, taxa: 0.04, retirada: 0.04 };
  const r = c.simular(p);
  assert.equal(r.meses, 300);
  perto(r.necessario, 1.8e6, 1e-6);
  perto(r.projetado, c.saldoFinal(50000, 1500, 0.04, 300), 1e-6);
  perto(r.falta, 1.8e6 - r.projetado, 1e-6);
  perto(c.saldoFinal(50000, r.aporteNecessario, 0.04, 300), 1.8e6, 1e-6, "aporte necessário atinge a meta");
  assert.ok(r.idadeChega > 60 && r.idadeChega < 100);
});

test("ir-fii-venda: comprou 100 a R$ 100, vendeu a R$ 110, sem custos → lucro R$ 1.000, IR R$ 200", () => {
  const c = F("ir-fii-venda");
  const r = c.irVendaFii({ pm: 100, venda: 110, qtd: 100, custos: 0, prejuizo: 0 });
  assert.equal(r.resultado, 1000);
  assert.equal(r.ir, 200);
  assert.equal(r.dedoDuro, 0, "0,005% de R$ 11.000 = R$ 0,55, dispensado por ser até R$ 1");
  assert.equal(r.darf, 200);
});

test("ir-fii-venda: custos, prejuízo anterior, dedo-duro e DARF mínimo", () => {
  const c = F("ir-fii-venda");
  const a = c.irVendaFii({ pm: 100, venda: 110, qtd: 100, custos: 10, prejuizo: 300 });
  assert.equal(a.resultado, 990); assert.equal(a.compensado, 300); perto(a.ir, 138, 1e-9); assert.equal(a.prejuizoRestante, 0);
  const b = c.irVendaFii({ pm: 100, venda: 110, qtd: 100, custos: 0, prejuizo: 1500 });
  assert.equal(b.ir, 0); assert.equal(b.prejuizoRestante, 500);
  const d = c.irVendaFii({ pm: 100, venda: 90, qtd: 100, custos: 0, prejuizo: 200 });
  assert.equal(d.resultado, -1000); assert.equal(d.ir, 0); assert.equal(d.prejuizoRestante, 1200);
  const e = c.irVendaFii({ pm: 100, venda: 120, qtd: 1000, custos: 0, prejuizo: 0 });
  perto(e.dedoDuro, 6, 1e-9); perto(e.darf, 3994, 1e-9);
  const f = c.irVendaFii({ pm: 100, venda: 102, qtd: 20, custos: 0, prejuizo: 0 });
  assert.equal(f.ir, 8); assert.equal(f.pagarAgora, false);
});

test("ir-fii-venda: vencimento do DARF no último dia útil do mês seguinte", () => {
  const c = F("ir-fii-venda");
  assert.equal(c.vencimentoDarf("2026-10-02"), "2026-11-30"); // segunda-feira
  assert.equal(c.vencimentoDarf("2026-07-15"), "2026-08-31"); // segunda-feira
  assert.equal(c.vencimentoDarf("2026-04-10"), "2026-05-29"); // 30 e 31/05 são fim de semana
  assert.equal(c.vencimentoDarf("2026-12-20"), "2027-01-29"); // 30 e 31/01/2027 são fim de semana
  assert.equal(c.vencimentoDarf("2024-02-05"), "2024-03-28"); // 29/03/2024 foi Sexta-feira Santa
  assert.equal(c.pascoa(2026).toISOString().slice(0, 10), "2026-04-05");
});
