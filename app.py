import streamlit as st
import requests
import graphviz

# Configuração da página
st.set_page_config(page_title="Gerador de Projeto com Análise de IA", layout="wide")
st.title("🧠 Gerador de Projeto com Análise de IA")

st.markdown("Cole abaixo um resumo da ideia do seu projeto, e receba um plano completo com fluxo, possibilidades de uso de IA, prompts e integrações.")

apiKey = "vVJjd0HIpUGcQ7pqP3pgQA"
url = "https://sai-library.saiapplications.com"
headers = {"X-Api-Key": apiKey}

# Entrada do usuário
resumo = st.text_area("✍️ Resumo da ideia do projeto", height=300)

if st.button("Gerar Projeto"):
    if not resumo.strip():
        st.warning("Por favor, insira um resumo do projeto.")
        st.stop()

    with st.spinner("Gerando etapas..."):

        
        prompt_parte_1 = f"""
Você é um especialista em UX, IA, automação, produtos digitais e arquitetura de soluções. A partir de uma breve descrição de qualquer projeto, sua tarefa é criar um planejamento completo, técnico e estratégico, avaliando se o projeto pode ou não utilizar IA, em quais pontos ela agrega valor e como poderia ser aplicada de forma segura, viável e útil.

📌 INSTRUÇÕES GERAIS:
Seja claro e objetivo em cada etapa, explicando apenas o essencial para orientar a implementação.

Utilize linguagem acessível, porém profissional e estratégica.

Gere respostas com subtítulos para cada item.
Seja objetivo e sintético. Responda cada seção com no máximo 3 a 5 bullets curtos.

Evite explicações longas, textos extensos ou aprofundamentos desnecessários.

Priorize aplicabilidade prática, clareza e resumo executivo.

Cada bullet deve ter no máximo 2 linhas.

NÃO gere:
- prompts para IA
- exemplos de prompt
- personas
- tom de voz
- instruções para chatbot
- exemplos conversacionais

✳️ FORMATAÇÃO OBRIGATÓRIA:
- Use markdown limpo
- Use títulos com ##
- Use listas com bullets
- NÃO use ###
- NÃO escreva textos gigantes sem quebra
- Separe todas as seções visualmente

✳️ INSTRUÇÃO FINAL:
Responda como um especialista técnico e estratégico, com clareza, objetividade e foco em aplicabilidade prática.

🧠 GERE APENAS OS TÓPICOS ABAIXO:

## Objetivo do Projeto
Explique claramente qual problema o projeto resolve, qual necessidade atende e qual o impacto esperado para usuários e empresa.

## O que o Projeto Resolve e Como
Descreva com profundidade como a solução funciona na prática.

Explique:
- processos automatizados
- ganhos operacionais
- redução de esforço manual
- melhorias na experiência do usuário

## Possibilidade de Utilizar IA (Sim ou Não)
Avalie se o projeto pode utilizar Inteligência Artificial.

Explique:
- Onde a IA pode ser aplicada
- Qual tipo de IA faz sentido
- Benefícios esperados
- Casos de uso possíveis

Considere:
- IA generativa
- Classificação automática
- Automação inteligente
- Predição
- OCR
- NLP
- Recomendação
- Análise de dados
- Assistentes virtuais

## Tipo Ideal de Solução
Explique qual o modelo ideal para implementação do projeto.

Exemplos:
- Sistema automatizado
- Plataforma híbrida
- Aplicação web
- Aplicativo
- Dashboard operacional
- Assistente virtual
- Fluxo automatizado
- Integração entre sistemas

Justifique tecnicamente.

## Pontos de Atenção
Liste riscos:
- Técnicos
- Operacionais
- UX
- Segurança
- Escalabilidade
- Custos
- Dependência de terceiros

Inclua ações preventivas.

Descrição do projeto:
{resumo}
"""

        data_1 = {
            "inputs": {
                "prompt": prompt_parte_1,
            }
        }

        response_1 = requests.post(
            f"{url}/api/templates/643388be603840da1c23b1b1/execute",
            json=data_1,
            headers=headers
        )

        if response_1.status_code == 200:
            conteudo_1 = response_1.text
        else:
            st.error(f"Erro na API (Parte 1): {response_1.status_code}")
            st.stop()

        prompt_parte_2 = f"""
Você é um especialista em UX, IA, automação, produtos digitais e arquitetura de soluções.

Abaixo está a análise estratégica inicial do projeto:

{conteudo_1}

Agora continue o planejamento seguindo TODAS as regras abaixo.

📌 INSTRUÇÕES GERAIS:
Seja claro e objetivo em cada etapa, explicando apenas o essencial para orientar a implementação.

Utilize linguagem acessível, porém profissional e estratégica.
Seja objetivo e sintético. Responda cada seção com no máximo 3 a 5 bullets curtos.

Evite explicações longas, textos extensos ou aprofundamentos desnecessários.

Priorize aplicabilidade prática, clareza e resumo executivo.

Cada bullet deve ter no máximo 2 linhas.

NÃO gere:
- prompts para IA
- exemplos de prompt
- personas
- tom de voz
- instruções para chatbot
- exemplos conversacionais

✳️ FORMATAÇÃO OBRIGATÓRIA:
- Use markdown limpo
- Use títulos com ##
- Use listas com bullets
- NÃO use ###
- NÃO escreva textos gigantes sem quebra
- Separe todas as seções visualmente

✳️ INSTRUÇÃO FINAL:
Responda como um especialista técnico e estratégico, com clareza, objetividade e foco em aplicabilidade prática.

🧠 GERE APENAS OS TÓPICOS ABAIXO:

## Planejamento de Falhas / Exceções
Descreva como o sistema deve reagir a:
- Erros de integração
- Dados inválidos
- Falha de API
- Ausência de resposta
- Instabilidade
- Fluxos inesperados

Inclua:
- contingência
- fallback
- monitoramento
- rastreabilidade
- logs
- alertas

## Desenho do Fluxo do Usuário
Descreva a jornada principal no formato:

[Início] → [Entrada de Dados] → [Processamento] → [Consulta/API] → [Resultado] → [Confirmação] → [Encerramento]

Ao final, gere também uma versão simplificada para diagrama visual.

IMPORTANTE:
- O fluxo simplificado deve ficar em uma linha
- Utilize "→"
- Não use markdown de lista nessa parte

## Estimativa de Tempo do Projeto
Crie uma estimativa macro de implementação dividida por etapas.

Considere:
- Levantamento de requisitos
- UX e arquitetura (se aplicável)
- Desenvolvimento
- Implementação de IA (se aplicável)
- Testes
- Homologação
- Deploy
- Monitoramento inicial

Para cada etapa:
- Explique rapidamente o objetivo
- Informe estimativa em horas
- Informe estimativa em dias considerando 1 dia = 8 horas

Ao final:
- Gere estimativa total consolidada
- Informe fatores que podem aumentar prazo
- Informe fatores que podem reduzir prazo

Descrição original do projeto:
{resumo}
"""

        data_2 = {
            "inputs": {
                "prompt": prompt_parte_2,
            }
        }

        response_2 = requests.post(
            f"{url}/api/templates/643388be603840da1c23b1b1/execute",
            json=data_2,
            headers=headers
        )

        if response_2.status_code == 200:
            conteudo_2 = response_2.text
        else:
            st.error(f"Erro na API (Parte 2): {response_2.status_code}")
            st.stop()

        conteudo = conteudo_1 + "\n\n" + conteudo_2

        # Separar texto do fluxo para virar imagem
        texto_projeto = conteudo
        fluxo_bruto = conteudo

        st.markdown("## 📋 Análise do Projeto Gerada")
        st.markdown(texto_projeto, unsafe_allow_html=True)

        # Geração do fluxo visual com graphviz
        st.markdown("## 🔄 Fluxo da Solução (visual)")
        with st.expander("Ver fluxo visual"):
            fluxo = graphviz.Digraph()

            linhas = fluxo_bruto.strip().split("\n")
            for linha in linhas:
                if "→" in linha:
                    etapas = [et.strip() for et in linha.split("→")]
                    for i in range(len(etapas) - 1):
                        fluxo.edge(etapas[i], etapas[i + 1])

            st.graphviz_chart(fluxo)

    st.success("✅ Projeto finalizado!!")
