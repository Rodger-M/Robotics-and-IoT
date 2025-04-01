import streamlit as st
import numpy as np
import time
import pandas as pd
from PIL import Image, ImageDraw

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa variáveis na sessão
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "ultima_temp" not in st.session_state:
    st.session_state.ultima_temp = 150  # Começa em 150°C

# Caminho da imagem da planta
img_path = "planta_do_forno.png"  # Certifique-se de que a imagem está nesse caminho

# Função para gerar dados simulados com comportamento progressivo
def gerar_dado():
    temperatura = st.session_state.ultima_temp

    if temperatura < 250:
        temperatura += np.random.uniform(2, 5)
    else:
        temperatura += np.random.uniform(-3, 3)
        if np.random.rand() < 0.03:
            temperatura += np.random.uniform(5, 10)

    temperatura = min(temperatura, 350)
    st.session_state.ultima_temp = temperatura

    status = "Aquecendo" if temperatura < 200 else "Estável"

    if temperatura > 300:
        st.session_state.alertas.append({"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura})
    
    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Função para gerar a imagem com o gradiente da temperatura
def gerar_imagem(temperatura):
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Define a cor com base na temperatura
    if temperatura < 200:
        cor = (0, 0, 255, 180)  # Azul
    elif temperatura < 250:
        cor = (0, 255, 0, 180)  # Verde
    else:
        vermelho = min(255, int((temperatura - 250) * 5))
        cor = (255, vermelho, 0, 180)  # De verde para vermelho

    # Desenha o gradiente no local do forno (600, 300)
    draw.ellipse((580, 280, 620, 320), fill=cor, outline=(0, 0, 0))

    # Redimensiona a imagem para 525x525
    img = img.resize((525, 525))
    
    return img

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Status Atual")
    status_metric = st.empty()
    
    st.subheader("⚠️ Alertas de Temperatura (>300°C)")
    alertas_display = st.empty()

with col2:
    st.subheader("🗺️ Localização do Forno")
    planta_display = st.empty()

st.subheader("📈 Evolução da Temperatura")
grafico_display = st.empty()

data = []  # Lista para armazenar os dados do gráfico

while True:
    novo_dado = gerar_dado()
    data.append(novo_dado)

    if len(data) > 20:
        data.pop(0)

    df = pd.DataFrame(data)

    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    if len(df) > 1:
        grafico_display.line_chart(df.set_index("timestamp")['temperature'])

    if len(st.session_state.alertas) > 0:
        df_alertas = pd.DataFrame(st.session_state.alertas)
        alertas_display.dataframe(df_alertas[::-1])
    else:
        alertas_display.text("Nenhum alerta registrado.")

    # Gera e exibe a imagem atualizada com o gradiente
    img_atualizada = gerar_imagem(novo_dado["temperature"])
    planta_display.image(img_atualizada, use_column_width=False)

    time.sleep(1)
