import streamlit as st
import openai
import graphviz

# Configuração da página
st.set_page_config(page_title="Gerador de Projeto de Bot", layout="wide")
st.title("🤖 Gerador de Projeto de Chatbot com IA")

st.markdown("Cole abaixo um resumo da ideia do seu bot, e receba um plano completo com fluxo, prompts e integrações.")

# 🔐 Sua chave da OpenAI (certifique-se de que ela está no secrets)
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Entrada do usuário
resumo = st.text_area("✍️ Resumo da ideia do bot", height=300)

if st.button("Gerar Projeto"):
    if not resumo.strip():
        st.warning("Por favor, insira um resumo do projeto.")
        st.stop()

    with st.spinner("Gerando etapas..."):

        resposta = client.chat.completions.create(
            model="gpt-4o",  # ou "gpt-4"
            messages=[
                {
                    "role": "system",
                    "content": (
                        """Você é um especialista em UX, IA e bots. A partir de uma breve descrição da ideia do projeto de chatbot, sua tarefa é criar um planejamento completo, técnico e estratégico, respondendo detalhadamente aos tópicos a seguir:

📌 INSTRUÇÕES GERAIS:
Seja detalhista em cada etapa, explicando com profundidade como será implementado.

Utilize linguagem acessível, porém profissional e estratégica.

Gere respostas com subtítulos para cada item, conforme os tópicos abaixo.

Na seção de prompts, gere exemplos prontos para IA generativa, com delimitadores claros e instruções embutidas no texto.

🧠 TÓPICOS PARA PLANEJAMENTO COMPLETO:
1. Nome da Persona
Caso o nome não seja fornecido, crie um nome adequado ao contexto da empresa ou serviço.

Justifique a escolha com base na função e tom do bot.

2. Tom de Voz
Defina o tom com até 3 palavras-chave (ex: Profissional, Empático, Acolhedor).

Descreva como esse tom se manifesta na linguagem (uso de emojis, jargões, expressões comuns, etc.).

3. O que o Bot Resolve e Como
Descreva, com profundidade, qual problema real esse bot resolve e como ele faz isso com clareza.

Enfatize os ganhos de eficiência, humanização e automatização.

4. Integrações Possíveis
Liste todas as APIs, sistemas internos ou externos que o bot pode se integrar.

Inclua: autenticação, CRM, ERPs, gateways de pagamento, busca por CPF/CNPJ, etc.

Para cada uma, descreva o benefício e o momento do fluxo em que será usada.

5. Possibilidade de Utilizar IA (Sim ou Não)
Explique se a IA generativa será usada e para quais finalidades específicas:

Interpretação de intenção

Resposta aberta

Classificação de entrada

Reação emocional

Simulação

Geração de mensagens

6. Tipo Ideal de Chatbot
Escolha entre: aberto, fechado, guiado ou misto.

Justifique com base no público, objetivo e nível de autonomia esperada.

7. Planejamento de Falhas / Evasivas
Descreva como o bot deve reagir a erros comuns:

Erro de sistema

Dados inválidos

Falta de resposta do usuário

Pedido fora do escopo

Crie respostas humanizadas e orientativas, com tom coerente com o bot.

8. Pontos de Atenção
Aponte riscos técnicos, UX e operacionais.

Indique medidas preventivas ou ações de monitoramento.

9. Desenho do Fluxo do Usuário
Descreva a jornada principal no formato:

css
Copiar
Editar
[Início] → [Identificação] → [Validação de dados] → [Consulta/Simulação] → [Escolha de Opção] → [Confirmação] → [Encerramento]
Ao final, converta o fluxo em uma versão simplificada para diagrama, com setas e caixas.

10. Dados Gerados pela Jornada
Liste quais dados serão capturados (ex: nome, CPF, status da solicitação, tipo de produto, etapa final).

Especifique como esses dados podem ser usados em relatórios e tomada de decisão.

11. Prompts para a IA (Formatados)
Crie ao menos 4 prompts de IA generativa, com estrutura clara e delimitadores.

Utilize o seguinte modelo:

shell
Copiar
Editar
## Prompt: {nome da tarefa}
### Objetivo:
{descrição do que a IA deve fazer}
### Entrada esperada:
{textos ou perguntas que o usuário pode fazer}
### Formato da Resposta:
{formato estruturado ou humanizado esperado}
### Exemplo de uso:
Usuário: {mensagem}
IA: {resposta ideal}
❗ Os prompts devem ser pensados para IA generativa em produção e cobrir casos reais de atendimento.

✳️ INSTRUÇÃO FINAL:
Responda a todos os tópicos como um especialista técnico e estratégico, com profundidade, exemplos práticos, e com aplicabilidade imediata para desenvolvimento ou apresentação de projeto."""
                    )
                },
                {"role": "user", "content": resumo}
            ],
            temperature=0.7
        )

        conteudo = resposta.choices[0].message.content

        # Separar texto do fluxo para virar imagem
        partes = conteudo.split("###")
        texto_projeto = ""
        fluxo_bruto = ""

        for parte in partes:
            if "fluxo" in parte.lower():
                fluxo_bruto = parte
            else:
                texto_projeto += "###" + parte

        st.markdown("## 📋 Projeto Gerado")
        st.markdown(texto_projeto)

        # Geração do fluxo visual com graphviz
        st.markdown("## 🔄 Fluxo do Usuário (visual)")
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
