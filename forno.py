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

# Usando st.empty para atualizar o gráfico sem recriar
chart_placeholder = st.empty()

# Exibe status e histórico fora do loop para evitar recriação
if "status_displayed" not in st.session_state:
    st.session_state.status_displayed = True
    st.subheader("📊 Status Atual")
    st.subheader("📋 Histórico de Dados")

# Inicializa as métricas e histórico
status_metric = st.empty()
historico_display = st.empty()

for _ in range(100):  # Executa 100 iterações (pode ser ajustado)
    novo_dado = gerar_dado()
    st.session_state.historico.append(novo_dado)

    # Limita o histórico a 20 registros
    if len(st.session_state.historico) > 20:
        st.session_state.historico.pop(0)

    # Criando DataFrame com os dados
    df = pd.DataFrame(st.session_state.historico)

    # Atualiza o gráfico de temperatura
    with col1:
        chart_placeholder.line_chart(df.set_index("timestamp")["temperature"])

    # Atualiza as métricas (status e temperatura)
    with col2:
        status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
        status_metric.subheader(f"Status: {novo_dado['status']}")

    # Atualiza o histórico de dados
    historico_display.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

    # Pausa para atualização a cada 1 segundo
    time.sleep(1)
