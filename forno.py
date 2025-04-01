import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Título
st.title("Monitoramento de Forno")

# Criando um dataframe para armazenar os dados simulados
data = pd.DataFrame(columns=["timestamp", "temperature", "status"])

# Função para simular temperatura e status
def gerar_dado():
    temperatura = np.random.uniform(100, 300)  # Temperatura entre 100°C e 300°C
    status = "Aquecendo" if temperatura < 200 else "Estável"
    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Loop para atualizar os dados em tempo real
placeholder = st.empty()  # Para atualizar sem recriar a página
historico = []

while True:
    # Gerando novos dados
    novo_dado = gerar_dado()
    historico.append(novo_dado)

    # Limitando histórico a 20 registros para não pesar
    if len(historico) > 20:
        historico.pop(0)

    # Criando um DataFrame com os dados
    df = pd.DataFrame(historico)

    # Layout em colunas
    col1, col2 = st.columns(2)

    # Gráfico de temperatura
    with col1:
        st.subheader("Temperatura do Forno")
        st.line_chart(df.set_index("timestamp")["temperature"])

    # Status atual
    with col2:
        st.subheader("Status Atual")
        st.metric(label="Temperatura", value=f"{novo_dado['temperature']:.2f} °C")
        st.metric(label="Status", value=novo_dado["status"])

    # Tabela de histórico
    with placeholder:
        st.subheader("Histórico de Dados")
        st.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

    time.sleep(1)  # Atualiza a cada 1 segundo
