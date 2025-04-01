import streamlit as st
import numpy as np
import time

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Função para gerar dados simulados
def gerar_dado():
    temperatura = np.random.uniform(100, 300)  # Temperatura entre 100°C e 300°C
    status = "Aquecendo" if temperatura < 200 else "Estável"
    return {"temperature": temperatura, "status": status}

# Exibe o título de Status Atual
st.subheader("📊 Status Atual")

# Usando st.empty() para atualizar as métricas sem recriar
status_metric = st.empty()

# Loop para atualizar o status a cada 1 segundo
for _ in range(100):  # Executa 100 iterações (pode ser ajustado)
    novo_dado = gerar_dado()

    # Atualiza as métricas de temperatura e status
    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    # Pausa para atualização a cada 1 segundo
    time.sleep(1)
