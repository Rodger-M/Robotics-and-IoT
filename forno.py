import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa o histórico de dados na sessão, se necessário
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função para gerar dados simulados
def gerar_dado():
    temperatura = np.random.uniform(100, 300)  # Temperatura entre 100°C e 300°C
    status = "Aquecendo" if temperatura < 200 else "Estável"
    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Layout das colunas
col1, col2 = st.columns(2)

# Exibe o gráfico e as métricas em um loop contínuo
chart_placeholder = st.empty()  # Para atualizar o gráfico sem recriar

for _ in range(100):  # Executa 100 iterações (pode ser ajustado)
    novo_dado = gerar_dado()
    st.session_state.historico.append(novo_dado)

    # Limita o histórico a 20 registros
    if len(st.session_state.historico) > 20:
        st.session_state.historico.pop(0)

    # Criando DataFrame com os dados
    df = pd.DataFrame(st.session_state.historico)

    with col1:
        st.subheader("🌡️ Temperatura do Forno")
        # Atualiza o gráfico sem recriar
        chart_placeholder.line_chart(df.set_index("timestamp")["temperature"])

    with col2:
        st.subheader("📊 Status Atual")
        st.metric(label="Temperatura", value=f"{novo_dado['temperature']:.2f} °C")
        st.metric(label="Status", value=novo_dado["status"])

    # Mostra o histórico de dados
    st.subheader("📋 Histórico de Dados")
    st.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

    # Pausa para atualizar a cada 1 segundo
    time.sleep(1)
