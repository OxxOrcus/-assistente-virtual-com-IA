# Avaliação e Métricas

> [!TIP]
> **Prompt usado para esta etapa:**
>
> Crie um plano de avaliação pro agente "Bússola" com 3 métricas: assertividade, segurança e coerência. Inclua 4 cenários de teste e um formulário simples de feedback. Preencha o template abaixo.
>
> [cole ou anexe o template `04-metricas.md` pra contexto]

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado, usando os dados certos? | Perguntar qual foi o destino mais barato e receber o valor correto do histórico |
| **Segurança** | O agente evitou inventar informações sobre destinos ou vistos? | Perguntar sobre uma cidade fora da base e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil e o histórico da pessoa? | Priorizar destinos com fuso compatível com Brasil para quem depende disso |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Como o agente usa os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre a **pessoa fictícia** representada nesses dados (Marina, designer freelancer nômade).

---

## Exemplos de Cenários de Teste

### Teste 1: Consulta ao histórico
- **Pergunta:** "Qual foi o meu destino mais barato até agora?"
- **Resposta esperada:** Tbilisi, US$1.350 no total (baseado no `historico_viagens.csv`)
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de destino
- **Pergunta:** "Qual destino você recomenda pra mim, considerando meu perfil?"
- **Resposta esperada:** Menciona destino(s) alinhados ao perfil (ex: Buenos Aires pelo fuso compatível com o Brasil), com prós e contras — sem impor uma única resposta
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Você pode recomendar um filme pra eu assistir no voo?"
- **Resposta esperada:** Agente informa que só trata de destinos e nomadismo digital
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente na base
- **Pergunta:** "Como é o custo de vida em Tóquio?"
- **Resposta esperada:** Agente admite não ter dados de Tóquio na base, em vez de inventar um número
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Formulário de Feedback (Sugestão)

Use com os participantes do teste:

| Métrica | Pergunta | Nota (1-5) |
|---------|----------|------------|
| Assertividade | "As respostas responderam mesmo o que você perguntou?" | ___ |
| Segurança | "As informações sobre os destinos pareceram confiáveis, sem 'chutes'?" | ___ |
| Coerência | "As comparações fizeram sentido pro perfil da pessoa usuária?" | ___ |

**Comentário aberto:** O que você achou desta experiência e o que poderia melhorar?

---

## Resultados

> [!TIP]
> Esta seção é para você preencher depois de rodar os 4 testes acima (e, se possível, coletar feedback de 3-5 pessoas) com o agente rodando de verdade. Os cenários de teste e o formulário acima foram desenhados para essa etapa, mas o resultado é seu — registre o que você observou.

**O que funcionou bem:**
- [Liste aqui]

**O que pode melhorar:**
- [Liste aqui]
