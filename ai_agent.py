# ai_agent.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Inicializa o modelo (pode ser ajustado para gpt-4o-mini, gemini, etc)
llm = ChatOllama(model="llama3.1", temperature=0.7)

def gerar_mensagem_ia(cliente, clima, motivo_alerta):
    """Usa a IA Generativa para redigir uma mensagem humanizada."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é o assistente virtual proativo de uma Seguradora. 
        Escreva um alerta curto tipo SMS (máximo 2 a 3 frases) alertando um segurado sobre uma condição climática.
        Seja empático, direto, previna danos e não cause pânico. 
        Use o perfil do cliente para deixar a mensagem extremamente personalizada."""),
        ("user", """
        Gere um SMS para o seguinte cliente:
        - Nome: {nome}
        - Cidade: {cidade}
        - Seguro Contratado: {seguro}
        - Perfil: {perfil}
        
        - Condição Climática Atual: {clima_desc} ({temp}°C)
        - Motivo do Alerta e Risco: {motivo}
        """)
    ])
    
    chain = prompt | llm
    
    resposta = chain.invoke({
        "nome": cliente["nome"],
        "cidade": cliente["cidade"],
        "seguro": cliente["seguro"],
        "perfil": cliente["perfil"],
        "clima_desc": clima["descricao"],
        "temp": clima["temperatura"],
        "motivo": motivo_alerta
    })
    
    return resposta.content