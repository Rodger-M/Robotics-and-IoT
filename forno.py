import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa o histórico de dados na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para gerar novos dados simulados
def gerar_dado():
    temperatura = np.random.uniform(100, 300)  # Temperatura entre 100°C e 300°C
    status = "Aquecendo" if temperatura < 200 else "Estável"
    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Adiciona novo dado ao histórico
novo_dado = gerar_dado()
st.session_state.historico.append(novo_dado)

# Mantém no máximo 20 registros
if len(st.session_state.historico) > 20:
    st.session_state.historico.pop(0)

# Criando um DataFrame com os dados
df = pd.DataFrame(st.session_state.historico)

# Layout da dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Temperatura do Forno")
    st.line_chart(df.set_index("timestamp")["temperature"])  # Atualiza sem recriar

with col2:
    st.subheader("📊 Status Atual")
    st.metric(label="Temperatura", value=f"{novo_dado['temperature']:.2f} °C")
    st.metric(label="Status", value=novo_dado["status"])

# Tabela de histórico
st.subheader("📋 Histórico de Dados")
st.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

# Atualiza automaticamente a cada 2 segundos
time.sleep(2)
st.experimental_rerun()
