import streamlit as st
import numpy as np
import time
import pandas as pd
from PIL import Image, ImageDraw

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa os históricos na sessão, se necessário
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "ultima_temp" not in st.session_state:
    st.session_state.ultima_temp = 150  # Inicia em 150°C para simular o aquecimento

# Função para gerar dados simulados com aquecimento progressivo
def gerar_dado():
    temperatura = st.session_state.ultima_temp

    # Se estiver abaixo de 250°C, sobe gradualmente
    if temperatura < 250:
        temperatura += np.random.uniform(2, 5)
    else:
        # Após estabilizar, pequenas variações normais (+-3°C)
        temperatura += np.random.uniform(-3, 3)

        # Para gerar um pico eventual, o aumento acontece progressivamente
        if np.random.rand() < 0.03:  # 3% de chance de começar um aumento
            temperatura += np.random.uniform(5, 10)  # Pequenos aumentos até passar de 300°C

    # Garante que a temperatura não passe de 350°C
    temperatura = min(temperatura, 350)

    # Atualiza o estado da última temperatura
    st.session_state.ultima_temp = temperatura

    status = "Aquecendo" if temperatura < 200 else "Estável"

    # Se a temperatura passar de 300°C, gera um alerta
    if temperatura > 300:
        st.session_state.alertas.append({"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura})

    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Função para gerar imagem da planta com indicador
def gerar_imagem(temperatura):
    img_path = "planta.png"  # Caminho da imagem da planta
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Define a cor do indicador
    if temperatura < 150:
        cor = (0, 0, 255, 150)  # Azul
    elif temperatura < 250:
        cor = (0, 255, 0, 150)  # Verde
    else:
        cor = (255, 0, 0, 150)  # Vermelho
    
    # Define posição do forno (ajustar conforme necessário)
    x, y = 600, 300
    draw.ellipse((x-20, y-20, x+20, y+20), fill=cor, outline=(0, 0, 0, 255))
    
    return img

# Layout em colunas
col1, col2 = st.columns([1, 2])  # Coluna 1 menor (Status + Alertas), Coluna 2 maior (Planta)

# ---- STATUS ----
with col1:
    st.subheader("📊 Status Atual")
    status_metric = st.empty()

    # ---- ALERTAS ----
    st.subheader("⚠️ Alertas de Temperatura (>300°C)")
    alertas_display = st.empty()

# ---- PLANTA ----
with col2:
    st.subheader("📍 Localização do Forno")
    planta_display = st.empty()

# ---- GRÁFICO ----
st.subheader("📈 Evolução da Temperatura")
grafico_display = st.empty()

# Loop infinito para gerar e atualizar os dados
while True:
    novo_dado = gerar_dado()

    # Atualiza o status
    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    # Atualiza o gráfico
    grafico_display.line_chart(pd.DataFrame(st.session_state.alertas).set_index("timestamp")["temperature"] if st.session_state.alertas else pd.DataFrame({"timestamp": [], "temperature": []}))

    # Atualiza a tabela de alertas
    if len(st.session_state.alertas) > 0:
        df_alertas = pd.DataFrame(st.session_state.alertas)
        alertas_display.dataframe(df_alertas[::-1])
    else:
        alertas_display.text("Nenhum alerta registrado.")

    # Atualiza a imagem da planta
    img_atualizada = gerar_imagem(novo_dado["temperature"])
    planta_display.image(img_atualizada, use_column_width=True)

    # Pausa para atualização
    time.sleep(1)
