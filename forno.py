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
    return {"temperature": temperatura, "status": status}

# Exibe o título de Status Atual
st.subheader("📊 Status Atual")

# Usando st.empty() para atualizar as métricas sem recriar
status_metric = st.empty()

# Exibe o título do Histórico de Dados
st.subheader("📋 Histórico de Dados")

# Usando st.empty() para exibir o histórico sem recriar a tabela
historico_display = st.empty()

# Loop para gerar e atualizar os dados
for _ in range(100):  # Executa 100 iterações (pode ser ajustado)
    novo_dado = gerar_dado()

    # Adiciona o novo dado ao histórico
    st.session_state.historico.append(novo_dado)

    # Limita o histórico a 20 registros
    if len(st.session_state.historico) > 20:
        st.session_state.historico.pop(0)

    # Atualiza o status (temperatura e status)
    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    # Atualiza a tabela de histórico
    df = pd.DataFrame(st.session_state.historico)
    historico_display.dataframe(df[::-1])  # Exibe o histórico mais recente no topo

    # Pausa para atualização a cada 1 segundo
    time.sleep(1)
