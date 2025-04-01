import streamlit as st
import numpy as np
import time
import pandas as pd

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

# Layout em colunas para organizar a interface
col1, col2 = st.columns(2)

# ---- STATUS ----
with col1:
    st.subheader("📊 Status Atual")
    status_metric = st.empty()  # Placeholder para atualizar os valores

# ---- HISTÓRICO ----
with col2:
    st.subheader("📋 Histórico de Dados")
    historico_display = st.empty()  # Placeholder para atualizar a tabela

# ---- GRÁFICO ----
st.subheader("📈 Evolução da Temperatura")
grafico_display = st.empty()  # Placeholder para o gráfico

# Loop para gerar e atualizar os dados
for _ in range(100):  # Executa 100 iterações (pode ser ajustado)
    novo_dado = gerar_dado()

    # Adiciona o novo dado ao histórico
    st.session_state.historico.append(novo_dado)

    # Limita o histórico a 20 registros
    if len(st.session_state.historico) > 20:
        st.session_state.historico.pop(0)

    # Converte o histórico para DataFrame
    df = pd.DataFrame(st.session_state.historico)

    # Atualiza o status (temperatura e status)
    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    # Atualiza a tabela de histórico
    historico_display.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

    # Atualiza o gráfico de temperatura
    if len(df) > 1:  # Garante que há dados suficientes para um gráfico
        grafico_display.line_chart(df.set_index("timestamp")["temperature"])

    # Pausa para atualização a cada 1 segundo
    time.sleep(1)
