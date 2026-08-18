import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_nomade.json'))
viagens = pd.read_csv('./data/historico_viagens.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
destinos = json.load(open('./data/destinos_nomades.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
PESSOA USUÁRIA: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_nomade']}
OBJETIVO: {perfil['objetivo_principal']}
ORÇAMENTO MENSAL: US$ {perfil['orcamento_mensal_usd']} | JÁ VISITOU: {', '.join(perfil['destinos_ja_visitados'])}
INTERESSE FUTURO: {', '.join(perfil['destinos_interesse_futuro'])}

HISTÓRICO DE VIAGENS:
{viagens.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

DESTINOS DISPONÍVEIS NA BASE DE CONHECIMENTO:
{json.dumps(destinos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Bússola, um assistente virtual que ajuda nômades digitais a escolherem o próximo destino para viver e trabalhar remotamente.

OBJETIVO:
Ajudar a pessoa usuária a comparar destinos e tomar uma decisão informada, usando o perfil, o histórico de viagens e a base de destinos fornecidos.

REGRAS:
- Use SOMENTE os destinos e dados presentes na base de conhecimento fornecida;
- NUNCA invente custo de vida, velocidade de internet, regras de visto ou qualquer dado sobre um destino que não esteja na base;
- Se o destino perguntado não estiver na base, admita isso claramente e sugira destinos parecidos que você conhece;
- Informação de visto é um ponto de partida, NÃO substitui a consulta a fontes oficiais (embaixada/consulado). Reforce isso sempre que o tema for visto ou documentação;
- Use o perfil e o histórico de viagens da pessoa para personalizar comparações;
- JAMAIS responda perguntas fora do tema de nomadismo digital e escolha de destinos. Quando ocorrer, lembre educadamente seu papel;
- Linguagem simples e acolhedora, como um amigo nômade mais experiente;
- Ajude a pessoa a decidir, mas a escolha final é sempre dela — apresente prós e contras, não imponha uma única resposta;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DA PESSOA USUÁRIA:
    {contexto}

    Pergunta: {msg}"""

    try:
        r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False}, timeout=60)
        r.raise_for_status()
        return r.json()['response']
    except requests.exceptions.ConnectionError:
        return ("Não consegui me conectar ao Ollama. Confirme se ele está rodando "
                "(`ollama serve`) e se o modelo foi baixado (`ollama pull gpt-oss`).")
    except requests.exceptions.RequestException as e:
        return f"Deu um erro ao falar com o modelo: {e}"

# ============ INTERFACE ============
st.title("🧭 Bússola, seu parceiro de destinos")
st.caption("Assistente para nômades digitais decidirem o próximo destino")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for autor, texto in st.session_state.mensagens:
    st.chat_message(autor).write(texto)

if pergunta := st.chat_input("Pergunte sobre destinos, custo de vida, visto, internet..."):
    st.session_state.mensagens.append(("user", pergunta))
    st.chat_message("user").write(pergunta)
    with st.spinner("Comparando destinos..."):
        resposta = perguntar(pergunta)
    st.session_state.mensagens.append(("assistant", resposta))
    st.chat_message("assistant").write(resposta)
