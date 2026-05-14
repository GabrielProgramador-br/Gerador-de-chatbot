import os
import json
import re
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Gerador de Projeto com Análise de IA", layout="wide")
st.title("🧠 Gerador de Projeto com Análise de IA")

st.markdown(
    "Cole abaixo um resumo da ideia do seu projeto e receba uma análise objetiva "
    "com foco em IA, ferramentas recomendadas, ganho estimado e referências."
)

TAVILY_API_KEY = "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"
SAI_API_KEY = "vVJjd0HIpUGcQ7pqP3pgQA"

SAI_URL = "https://sai-library.saiapplications.com/api/templates/643388be603840da1c23b1b1/execute"


def buscar_informacoes_tavily(query, max_results=5):
    if not TAVILY_API_KEY:
        return "", []

    url = "https://api.tavily.com/search"

    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()

        results = response.json().get("results", [])

        contexto = "\n\n".join(
            [
                f"Fonte: {item.get('url')}\nTítulo: {item.get('title')}\nConteúdo: {item.get('content')}"
                for item in results
            ]
        )

        fontes = [
            {
                "titulo": item.get("title"),
                "url": item.get("url"),
                "conteudo": item.get("content")
            }
            for item in results
            if item.get("url")
        ]

        return contexto, fontes

    except Exception as e:
        st.warning(f"Não foi possível consultar a Tavily: {e}")
        return "", []


def chamar_sai(prompt):
    data = {
        "inputs": {
            "prompt": prompt,
        }
    }

    headers = {
        "X-Api-Key": SAI_API_KEY
    }

    try:
        response = requests.post(SAI_URL, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text

    except Exception as e:
        st.error(f"Erro ao consultar SAI Data: {e}")
        return None


def extrair_json(texto):
    try:
        return json.loads(texto)
    except Exception:
        pass

    match = re.search(r"\{.*\}", texto, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def gerar_top_5_ferramentas(resumo):
    prompt = f"""
Você é um especialista em IA, automação e arquitetura de soluções.

Com base no projeto abaixo, recomende exatamente 5 ferramentas/plataformas de IA adequadas.

Responda exclusivamente em JSON válido, sem markdown, sem explicações e sem texto fora do JSON.

Formato obrigatório:
{{
  "ferramentas": [
    {{
      "nome": "Nome da ferramenta",
      "motivo": "Por que ela faz sentido para o projeto"
    }}
  ]
}}

Regras:
- Retorne exatamente 5 ferramentas.
- Use ferramentas reais e conhecidas.
- Não invente ferramentas.
- Não inclua links nesta etapa.

Descrição do projeto:
{resumo}
"""

    resposta = chamar_sai(prompt)

    if not resposta:
        return []

    dados = extrair_json(resposta)

    if not dados:
        st.warning("Não foi possível interpretar o JSON de ferramentas retornado pela SAI.")
        return []

    return dados.get("ferramentas", [])[:5]


def buscar_referencias_por_ferramenta(ferramentas, resumo):
    referencias = {}

    for ferramenta in ferramentas:
        nome = ferramenta.get("nome")

        if not nome:
            continue

        query = (
            f"{nome} official documentation AI automation productivity use cases "
            f"benefits efficiency implementation {resumo[:150]}"
        )

        contexto, fontes = buscar_informacoes_tavily(query, max_results=3)

        referencias[nome] = {
            "contexto": contexto,
            "fontes": fontes
        }

    return referencias


def formatar_referencias_por_ferramenta(referencias):
    blocos = []

    for nome, dados in referencias.items():
        fontes = dados.get("fontes", [])

        fontes_formatadas = "\n".join(
            [
                f"- {fonte.get('titulo') or 'Sem título'}: {fonte.get('url')}\n  Trecho: {fonte.get('conteudo')}"
                for fonte in fontes
            ]
        )

        if not fontes_formatadas:
            fontes_formatadas = "- Nenhuma referência encontrada."

        blocos.append(
            f"""
Ferramenta: {nome}
Referências encontradas:
{fontes_formatadas}
"""
        )

    return "\n\n".join(blocos)


def processar_com_sai_data(resumo, referencias_por_ferramenta):
    referencias_formatadas = formatar_referencias_por_ferramenta(referencias_por_ferramenta)

    prompt = f"""
Você é um especialista em IA, automação, arquitetura de soluções e produtos digitais.

A partir da descrição do projeto e das referências específicas por ferramenta, gere uma análise objetiva e estratégica.

📌 REGRAS:
- Seja extremamente direto
- Use markdown limpo
- Use apenas títulos ##
- Responda com bullets curtos
- Não gere textos longos
- Não gere fluxo
- Não gere planejamento
- Não gere prompts
- Não gere personas
- Não gere UX
- Não gere arquitetura detalhada
- Sempre inclua o ganho estimado em porcentagem
- Cada ferramenta obrigatoriamente precisa ter pelo menos uma referência com link
- Use as referências específicas de cada ferramenta
- Não use uma referência genérica para todas as ferramentas
- Se uma ferramenta não tiver referência encontrada, informe: "Referência direta não encontrada via Tavily"
- Mesmo quando a referência direta não for encontrada, mantenha a ferramenta e sinalize que o ganho é uma estimativa baseada no potencial de automação

⚠️ GERE APENAS OS TÓPICOS ABAIXO:

## Objetivo do Projeto
Explique:
- Qual problema resolve
- Qual necessidade atende
- Impacto esperado
- Ganhos operacionais
- Benefício para usuários e empresa

## Possibilidade de Utilizar IA
Avalie como IA pode ser utilizada no projeto.

Para cada possibilidade:
- Explique rapidamente o uso
- Explique o benefício esperado

## Top 5 Ferramentas Recomendadas

Para cada ferramenta informe obrigatoriamente:
- Nome da ferramenta
- Como seria utilizada no projeto
- Tipo de IA utilizada
- Benefício operacional
- Facilidade de implementação
- Ganho estimado de produtividade/eficiência em porcentagem
- Referência usada para embasar o ganho estimado, com link

## Referências Consultadas
Liste todas as fontes utilizadas, agrupadas por ferramenta.

Descrição do projeto:
{resumo}

Referências específicas por ferramenta:
{referencias_formatadas}
"""

    return chamar_sai(prompt)


resumo = st.text_area("✍️ Resumo da ideia do projeto", height=300)

if st.button("Gerar Projeto"):
    if not resumo.strip():
        st.warning("Por favor, insira um resumo do projeto.")
        st.stop()

    if not TAVILY_API_KEY:
        st.error("A variável TAVILY_API_KEY não foi encontrada no arquivo .env.")
        st.stop()

    if not SAI_API_KEY:
        st.error("A variável SAI_API_KEY não foi encontrada no arquivo .env.")
        st.stop()

    with st.spinner("Identificando ferramentas recomendadas..."):
        ferramentas = gerar_top_5_ferramentas(resumo)

    if not ferramentas:
        st.error("Não foi possível gerar a lista de ferramentas.")
        st.stop()

    with st.spinner("Buscando referências específicas para cada ferramenta..."):
        referencias_por_ferramenta = buscar_referencias_por_ferramenta(ferramentas, resumo)

    with st.spinner("Gerando análise final..."):
        conteudo = processar_com_sai_data(resumo, referencias_por_ferramenta)

    if conteudo:
        st.markdown("## 📋 Análise do Projeto Gerada")
        st.markdown(conteudo, unsafe_allow_html=True)

    st.success("✅ Análise finalizada!")