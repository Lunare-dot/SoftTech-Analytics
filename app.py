import streamlit as st
from src.layers.data import loader, cleaner
from src.layers.presentation.dashboard import show_dashboard

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SoftTech Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CARREGAMENTO E LIMPEZA DE DADOS
@st.cache_data
def load_and_clean_data():
    df_raw = loader.load_raw_data()
    return cleaner.clean(df_raw)

try:
    df = load_and_clean_data()
except Exception as e:
    st.error(f"Erro ao carregar a base de dados: {e}")
    st.stop()
    
if df.empty:
    st.error("Base de dados vazia ou indisponível no momento.")
else:
    show_dashboard(df)