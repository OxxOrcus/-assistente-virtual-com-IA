# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
>
> Organize a base de conhecimento do agente "Bússola" usando os 4 arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>
> [cole ou anexe o template `02-base-conhecimento.md` pra contexto]

## Dados Utilizados

| Arquivo | Formato | Para que serve no Bússola? |
|---------|---------|---------------------|
| `perfil_nomade.json` | JSON | Personalizar comparações e recomendações com base no orçamento, preferências e objetivo atual da pessoa usuária. |
| `historico_viagens.csv` | CSV | Contextualizar destinos onde a pessoa já morou, quanto gastou e como avaliou cada experiência. |
| `historico_atendimento.csv` | CSV | Dar continuidade a dúvidas anteriores, evitando repetir do zero um assunto já discutido. |
| `destinos_nomades.json` | JSON | Base principal de destinos "nômade-friendly", com custo de vida, internet, visto, segurança e comunidade — é daqui que o agente tira quase todas as respostas sobre lugares. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados?

Sim. O tema original do repositório de exemplo é um educador financeiro; para o meu agente, recriei os quatro arquivos do zero com um tema de nomadismo digital. Mantive o mesmo número de arquivos e um formato parecido (um perfil de usuário, dois históricos e uma base "de produtos"), mas troquei todo o conteúdo: em vez de produtos financeiros, `destinos_nomades.json` traz 7 cidades com custo de vida, internet, visto, segurança e comunidade. Deixei de propósito uma cidade do interesse da pessoa usuária (Cidade do Cabo) fora da base, para poder testar se o agente admite quando não tem dados suficientes em vez de inventar.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos são carregados no início da sessão, direto do disco, como no exemplo abaixo:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_nomade.json'))
viagens = pd.read_csv('./data/historico_viagens.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
destinos = json.load(open('./data/destinos_nomades.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para manter o protótipo simples, os quatro arquivos são injetados inteiros no prompt a cada pergunta, garantindo que o agente sempre tenha o contexto completo disponível. Em uma versão mais robusta, o ideal seria consultar apenas os destinos relevantes para a pergunta (busca/RAG), reduzindo o consumo de tokens.

```text
PERFIL DA PESSOA USUÁRIA (data/perfil_nomade.json):
{
  "nome": "Marina Costa",
  "idade": 29,
  "profissao": "Designer UX Freelancer",
  "renda_mensal_usd": 3200.00,
  "perfil_nomade": "intermediario",
  "objetivo_principal": "Escolher o próximo destino para os próximos 2-3 meses, equilibrando custo de vida, comunidade e fuso horário de trabalho",
  "orcamento_mensal_usd": 1500.00,
  "paises_visitados_como_nomade": 6,
  "preferencias": {
    "clima": "ameno a quente, sem umidade excessiva",
    "importancia_internet": "alta (faz videochamadas quase todo dia)",
    "importancia_comunidade": "alta",
    "fuso_horario_trabalho": "precisa de sobreposição com Brasil (UTC-3) e, se possível, Europa (UTC+0/+1)"
  },
  "destinos_ja_visitados": ["Lisboa", "Medellín", "Cidade do México", "Bali", "Chiang Mai", "Tbilisi"],
  "destinos_interesse_futuro": ["Buenos Aires", "Cidade do Cabo"]
}

HISTORICO DE VIAGENS (data/historico_viagens.csv):
data_inicio data_fim   cidade           pais      custo_total_usd categoria_gasto_principal avaliacao
2025-09-01  2025-10-15 Lisboa           Portugal  3200.00          hospedagem                5
2025-10-20  2025-12-05 Medellín         Colômbia  1800.00          alimentacao               4
2025-12-10  2026-01-25 Cidade do México México    2400.00          hospedagem                4
2026-02-01  2026-03-20 Bali             Indonésia 2000.00          coworking                 5
2026-03-25  2026-05-10 Chiang Mai       Tailândia 1500.00          hospedagem                5
2026-05-15  2026-07-01 Tbilisi          Geórgia   1350.00          transporte                4

HISTORICO DE ATENDIMENTO (data/historico_atendimento.csv):
data       canal  tema           resumo                                                                     resolvido
2025-10-10 chat   Visto          Dúvida sobre requisitos do visto D8 em Portugal                            sim
2025-12-01 chat   Internet       Pergunta sobre estabilidade de internet em Medellín para chamadas de vídeo  sim
2026-02-05 email  Comunidade     Buscou grupos e eventos de nômades digitais em Bali                         sim
2026-04-15 chat   Custo de vida  Comparação de custo entre Chiang Mai e Tbilisi                               sim
2026-07-20 chat   Fuso horário   Dúvida sobre sobreposição de horário com clientes no Brasil na Ásia          sim

BASE DE DESTINOS (data/destinos_nomades.json):
[
  {
    "cidade": "Lisboa", "pais": "Portugal", "custo_vida_mensal_usd": 1800,
    "internet_media_mbps": 150, "fuso_horario": "UTC+0", "visto_nomade": "D8 - Visto Nômade Digital",
    "indice_seguranca": "alto", "comunidade_nomades": "grande e muito ativa"
  },
  {
    "cidade": "Medellín", "pais": "Colômbia", "custo_vida_mensal_usd": 1200,
    "internet_media_mbps": 100, "fuso_horario": "UTC-5", "visto_nomade": "Visto V - Nómada Digital",
    "indice_seguranca": "medio", "comunidade_nomades": "grande e ativa"
  },
  "... (mais 5 destinos: Cidade do México, Bali, Chiang Mai, Tbilisi e Buenos Aires)"
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo abaixo sintetiza os dados originais, mantendo só o que é mais relevante para uma pergunta típica, o que ajuda a economizar tokens. Ainda assim, o mais importante continua sendo garantir que todas as informações relevantes estejam disponíveis no contexto.

```
PERFIL:
- Nome: Marina Costa
- Perfil: Intermediário | Orçamento: US$ 1.500/mês
- Objetivo: escolher o próximo destino (2-3 meses), priorizando internet, comunidade e fuso com Brasil/Europa
- Já visitou: Lisboa, Medellín, Cidade do México, Bali, Chiang Mai, Tbilisi

DESTINO MAIS BARATO JÁ VISITADO: Tbilisi (US$ 1.350 no total)

DESTINOS DISPONÍVEIS PARA COMPARAR:
- Lisboa (US$1.800/mês, internet 150 Mbps, UTC+0, visto D8, comunidade grande)
- Medellín (US$1.200/mês, internet 100 Mbps, UTC-5, visto V, comunidade grande)
- Cidade do México (US$1.400/mês, internet 90 Mbps, UTC-6, sem visto específico)
- Bali (US$1.300/mês, internet 40 Mbps, UTC+8, visto E33G/Second Home)
- Chiang Mai (US$1.000/mês, internet 80 Mbps, UTC+7, visto DTV)
- Tbilisi (US$900/mês, internet 60 Mbps, UTC+4, isenção de visto)
- Buenos Aires (US$1.000/mês, internet 70 Mbps, UTC-3, Visa Nómada Digital)
```
