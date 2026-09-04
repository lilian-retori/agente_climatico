import streamlit as st
import time
from mock_db import get_clientes
from weather_service import obter_dados_climaticos
from rules_engine import verificar_necessidade_alerta
from ai_agent import gerar_mensagem_ia

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA)
st.set_page_config(page_title="ProtegeSeguro IA", page_icon="🛡️", layout="wide")

# 2. Injeção de CSS Customizado (ESTILO AGÊNCIA DE UI/UX MODERNA)
st.markdown("""
<style>
    /* Importando fonte moderna e elegante */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Reset de fonte para a página toda */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo Dark Premium (Modo Escuro com leve gradiente radial) */
    .stApp {
        background-color: #0b0f19;
        background-image: radial-gradient(circle at 15% 50%, rgba(20, 50, 100, 0.15), transparent 25%),
                          radial-gradient(circle at 85% 30%, rgba(0, 198, 255, 0.1), transparent 25%);
        color: #e2e8f0;
    }

    /* Estilo dos Cartões - Efeito Glassmorphism (Vidro) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(18, 25, 43, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease-in-out;
    }
    
    /* Efeito de Hover (passar o mouse) nos Cartões */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border: 1px solid rgba(0, 198, 255, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 10px 40px 0 rgba(0, 198, 255, 0.15);
    }

    /* Títulos e Textos */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    p, span, div {
        color: #94a3b8;
    }

    /* Botão Primário Moderno (Estilo Neon/Glow) */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
        transform: scale(1.02);
    }
    
    /* Estilizando o Sidebar */
    [data-testid="stSidebar"] {
        background-color: #060a11 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Esconde o menu padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Cabeçalho com Logo Textual Neon
col_logo, col_texto = st.columns([1, 15])
with col_logo:
    st.markdown("<h1 style='text-align: center; color: #00C6FF; margin-top: -10px;'>⚡</h1>", unsafe_allow_html=True)
with col_texto:
    st.markdown("<h2 style='color: #ffffff; margin-top: -20px; margin-bottom: 0px;'>ProtegeSeguro <span style='color: #00C6FF;'>AI</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 16px;'>Plataforma Inteligente de Prevenção de Sinistros</p>", unsafe_allow_html=True)

st.write("") 

# 4. Sidebar (CRM Simulado)
clientes = get_clientes()
with st.sidebar:
    st.markdown("<h3 style='color: #ffffff;'>💼 Carteira de Clientes</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #00C6FF; font-weight: bold;'>{len(clientes)} segurados ativos.</p>", unsafe_allow_html=True)
    st.dataframe(clientes, hide_index=True)
    st.caption("Fonte: clientes.csv")

# 5. Ação Principal
if st.button("▶ Executar Varredura Inteligente", type="primary"):
    
    progress_bar = st.progress(0, text="Sincronizando satélites meteorológicos...")
    total_clientes = len(clientes)
    
    st.write("---")
    
    # Grid de 3 em 3
    colunas_por_linha = 3
    
    for i in range(0, total_clientes, colunas_por_linha):
        cols = st.columns(colunas_por_linha)
        trio_clientes = clientes[i : i + colunas_por_linha]
        
        for j, cliente in enumerate(trio_clientes):
            with cols[j]: 
                with st.container(border=True):
                    # Cabeçalho do Cartão
                    st.markdown(f"<h4 style='color: white;'>{cliente['nome']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #00C6FF; font-size: 14px;'>📍 {cliente['cidade']}</span> | <span style='color: #e2e8f0; font-size: 14px;'>{cliente['seguro']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='font-size:12px; color:#64748b;'>{cliente['perfil']}</span>", unsafe_allow_html=True)
                    st.divider()
                    
                    with st.spinner("Buscando dados climáticos..."):
                        clima = obter_dados_climaticos(cliente['cidade'])
                    
                    if not clima:
                        st.error("Falha de conexão com satélite.")
                        continue
                        
                    # Métrica
                    st.metric(
                        label="Clima Local", 
                        value=f"{clima['temperatura']} °C", 
                        delta=clima['descricao'].capitalize(),
                        delta_color="off"
                    )
                    
                    enviar_alerta, motivo = verificar_necessidade_alerta(cliente, clima)
                    
                    if enviar_alerta:
                        st.warning(f"Risco: {motivo}", icon="⚠️")
                        with st.spinner("Gerando notificação..."):
                            mensagem = gerar_mensagem_ia(cliente, clima, motivo)
                        st.info(f"📱 SMS:\n\n{mensagem}")
                    else:
                        st.success("Sem riscos detectados.", icon="✅")
                        
            progress_bar.progress((i + j + 1) / total_clientes, text=f"Analisando perfil {i+j+1} de {total_clientes}...")
            time.sleep(0.3) 
            
    progress_bar.empty()
    st.markdown("<h4 style='color: #00C6FF; text-align: center;'>✅ Varredura Neural Concluída!</h4>", unsafe_allow_html=True)