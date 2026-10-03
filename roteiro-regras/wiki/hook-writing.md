---
name: Hook Writing Patterns & Performance
description: Weekly documented patterns from engagement-analyzer ritual. What works, what doesn't, ranked by impact.
type: semantic
updated: 2026-08-02
sources: ["[[episodic/analysis/analysis-2026-05-04]]"]
tags: [content, hooks, patterns, measurement]
---

# Hook Writing Patterns

**Purpose**: Central registry of what hook patterns work. Updated weekly from engagement-analyzer ritual. Used by hook-generation.md to propose variants, by tone-enforcer.md to rank quality.

---

## Week of April 24-28, 2026 (Infrastructure Validation)

### Confirmed Patterns (Test Data — Production Confirmation Needed)

**Pattern 1: Contrast + Number in First 5 Words** 🎯 **STRONG**

- **Impact**: +57% above baseline (ranging +33% to +81%)
- **Data**: 2 posts, April 24-28
- **Confidence**: HIGH
- **Platform**: X (primary), TikTok (secondary)
- **Example**: "Selic hit 14.25%. Your savings just got 50% more profitable. Your debt just got 50% more expensive."
- **Mechanism**: Hits nervous system directly (gain vs pain, simultaneous contrast)
- **Sample posts**: 
  - post-001: 3.8% engagement (post-001 at +81%)
  - post-008: 2.8% engagement (+33%)
- **Test status**: PRIORITY 1 — ready to execute May 5-11
- **Next test**: Scale to 5 posts, confirm pattern holds at scale. Success threshold: avg ≥3.0% engagement

---

**Pattern 2: Specific Numbers > Generic Language** 📊 **MEDIUM**

- **Impact**: +20% on LinkedIn (specific numbers dominate generic language)
- **Data**: 2 LinkedIn posts, April 24-28
- **Confidence**: MEDIUM (small sample, but clear direction)
- **Platform**: LinkedIn-specific signal (may not transfer to X/IG)
- **Example (Good)**: "Tech workers: 14.25% Selic = $1,425/month on $100k, zero stock risk"
- **Example (Bad)**: "Tech workers: High rates are a gut-check. Savings as return vehicle."
- **Sample posts**:
  - post-006: 3.11% engagement (specific numbers, +20% vs baseline)
  - post-002: 2.33% engagement (generic language, -10% vs baseline)
- **Test status**: PRIORITY 2 — ready for May 8-11 (if PRIORITY 1 succeeds)
- **Next test**: 3 LinkedIn posts with specific Selic/$ numbers. Success threshold: avg ≥2.9%

---

### Patterns to Avoid

**Generic Tips / Vague Language** ❌ **NEGATIVE**

- **Impact**: -44% below baseline
- **Data**: 1 post (post-007), April 27
- **Confidence**: MEDIUM (only 1 post, but dramatic underperformance)
- **Example (Bad)**: "Save money tips: High interest rates are good. You should put money in savings. Interest rates matter. Remember to save!"
- **Why it fails**: No contrast, no specificity, no emotional hook, no clear benefit statement
- **Action**: AVOID. Do not test or replicate this pattern.
- **Monitoring**: If 2+ additional posts confirm -40%+ underperformance, lock as "DO NOT USE" rule

---

## Testing Recommendations (May 5-11)

### TIER 1: Contrast + Number Scaling

**Hypothesis**: Contrast + Number pattern holds at scale (5 posts)

**Control**: Random mix of hooks (baseline)

**Treatment**: All 5 posts open with "contrast + number" format

**Sample**: 5 posts on X, May 5-11

**Success criteria**: Average engagement ≥3.0% (vs baseline 2.1%)

**Rollback**: If avg <2.4%, revert to mixed hooks

**Priority**: 🔴 EXECUTE NOW

---

### TIER 2: LinkedIn Specific Numbers (Secondary)

**Hypothesis**: Specific Selic rates + $ examples outperform generic language by >15%

**Control**: Generic interest rate language

**Treatment**: Specific numbers (14.25%, $1,425/month, etc.)

**Sample**: 3 LinkedIn posts, May 8-11 (only if TIER 1 succeeds)

**Success criteria**: Average engagement ≥2.9%

**Priority**: 🟡 EXECUTE IF TIER 1 CONFIRMS

---

## Methodology Notes

- **Measurement**: engagement_rate = (likes + retweets/comments + saves) / impressions
- **Baseline**: Historical 4-week average (April 1-28) per platform
  - X: 2.1%
  - Instagram: 1.8%
  - LinkedIn: 2.6%
- **Performance score**: (this_week / baseline) × 100
  - >100 = above baseline
  - <100 = below baseline
- **Confidence**: Based on sample size
  - HIGH: 3+ data points, consistent direction
  - MEDIUM: 2 data points, or inconsistent direction
  - LOW: 1 data point

---

## Key Insights (So Far)

1. **Contrast is a nervous system hijack** — The brain notices contradictions (savings + debt cost, rate risk + security). Use this.
2. **Specificity > Generality** — "$1,425/month" > "good interest rates". Numbers are trustworthy. Vagueness is not.
3. **Platform matters** — LinkedIn rewards economic + thought leadership. X rewards contrast + provocation. IG rewards visual + personal.
4. **The formula**: SETUP (contrast: savings pain/gain) → TENSION (debt cost) → PUNCH (the number, the proof)

---

## Weekly Update Cadence

**Updated**: Every Sunday, 10:00 UTC (after engagement-analyzer ritual)

**What changes**:
- New patterns added (if significant, >5% impact difference from baseline)
- Confidence levels updated (as sample size grows)
- Test results logged (TIER 1 results → TIER 2 proposed → TIER 3 locked)

**What stays**: Proven patterns from prior weeks (cumulative, never removed unless explicitly contradicted)

---

---

## Frameworks Externos — Hana Frank (Ciência do Conteúdo)

*Ingerido 2026-05-18. Fonte: [[sources/hana-frank-conteudo-viral-ciencia]]*

### Estrutura IHC (Identificação → História → Conteúdo)
1. **Identificação**: começa com assunto amplo que gera familiaridade (conflito universal — traição, injustiça, ambição)
2. **História**: prova o ponto que você quer fazer
3. **Conteúdo**: moral da história = o que você quer vender/ensinar

### Estrutura Jeito Errado → Jeito Certo
Conflito → Jeito errado (como o público faz hoje) → Processo de virada → Jeito certo → Moral da história

*Por que funciona: mostrar o jeito errado demonstra autoridade implicitamente. O público se identifica ("é isso que eu faço!") e quer descobrir o jeito certo.*

### Gatilhos viciantes (manter atenção até o final)
- **Familiaridade**: citar expressões, memes, livros famosos que o público reconhece
- **Contraste de emoções**: altos e baixos no roteiro. Faz pensar uma coisa, depois outra.

### Princípio da Interseção Criativa
Comece com tema que 100% do público se interessa (traição, dinheiro, relacionamento) → guie para o tema do seu nicho. O overlap entre dois círculos temáticos é o ângulo certo do roteiro.

**Aplicação Investir e Cocar**: começar com conflito universal ("seu salário não acompanha a Selic", "você economiza mas não fica rico") → conectar com o conceito financeiro do vídeo.

---

**Owner**: TANAKA BRAIN (analysis), CURATOR (measurement)  
**Input**: engagement-analyzer.md weekly ritual  
**Output**: Used by hook-generation.md, tone-enforcer.md, CLAUDE.md rules  
**Sync**: Auto-synced from episodic/analysis/analysis-YYYY-MM-DD.md files


## Semana de 2026-05-02 a 2026-05-09

**Melhor hook X** (+17.9% vs baseline 2.1%)
> `**Status:** Material bruto — PaperClip cria o conteúdo`
- 👍 0  🔁 0  💬 1  👁 5
- Todos acima da baseline: 3 de 3 posts


## Semana de 2026-07-18 a 2026-07-25

**Melhor hook IG** (+0.1% vs baseline 1.8%)
> `> Tanaka, enquanto todo mundo foge da bolsa brasileira, o banco mais desconfiado de Wall Street virou comprador pesado.`
- 👍 248  💾 52  💬 12  👁 16783

## Regra: Contraste exige 2 números

Quando o padrão dominante da semana é CONTRASTE (lado A esperado vs lado B real), o hook precisa dos dois números, não de um só. Um número sozinho vira acusação solta e perde força — os dois juntos é que fazem o contraste funcionar (ex: "China apagou 20 anos de valorização imobiliária em 12 meses" só bate combinando o número institucional/esperado com o número real/inesperado). *(derivado de Reflexão do CURATOR em 2026-07-29, JAP-7739)*


## Semana de 2026-07-26 a 2026-08-02

**Melhor hook IG** (+0.5% vs baseline 1.8%)
> `O brasileiro está mais endividado hoje do que estava em 2014 — véspera da pior recessão do século. O alerta é do BTG, ba`
- 👍 280  💾 27  💬 32  👁 14829

## Molde: Denúncia institucional + 2 números (Shorts)

*Identificado via radar de outliers do nicho, 2026-08-04. Fonte: A Cara da Riqueza — "Será que alugar é a melhor opção?" — 3.9x, 140.017 views (short, 7d). [JAP-7968]*

**Estrutura**: `[instituição] quer/vende/esconde X, você/sua conta ganha Y` — número concreto de cada lado (ex: 30 anos vs CDI, R$600 mil vs chave, 0,3% ao mês). Denúncia + matemática simples nos primeiros segundos, sem enrolação.

- **Por que funciona**: mesmo mecanismo do "Regra: Contraste exige 2 números" acima (um número solto vira acusação vaga; dois números batendo um contra o outro é que sustentam o hook), mas com o antagonista nomeado como instituição (banco, mercado imobiliário) em vez de dado macro.
- **Aplicação**: molde de embalagem para Shorts — testar título/hook nesse formato, não copiar o tema do outlier (alugar vs financiar já é roteiro long-form em issue separada).
- **Status**: 1 outlier confirmado, ainda sem teste A/B próprio no canal. Testar como PRIORIDADE 1 no próximo Short com antagonista institucional claro.
