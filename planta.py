import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Carrega a planta (substitua com o caminho correto da imagem)
img_path = "planta_industria.png"  # Substitua pelo caminho da sua imagem
img = Image.open(img_path)

# Definindo o centro do forno na planta (exemplo de coordenadas x, y)
forno_x, forno_y = 600, 300  # Ajuste conforme a localização do forno na sua imagem

# Função para adicionar um círculo com gradiente
def adicionar_gradiente(imagem, x, y, raio=40):
    # Criação de uma imagem de gradiente circular
    tamanho = (raio * 2, raio * 2)
    gradiente = Image.new("RGBA", tamanho, (0, 0, 0, 0))

    # Cria um gradiente radiante
    draw = ImageDraw.Draw(gradiente)
    for i in range(raio, 0, -1):
        alpha = int(255 * (1 - i / raio))  # Degradê de transparência
        draw.ellipse((raio - i, raio - i, raio + i, raio + i), fill=(255, 0, 0, alpha))

    # Aplica o gradiente sobre a imagem original
    imagem.paste(gradiente, (x - raio, y - raio), gradiente)
    return imagem

# Adicionando o gradiente ao ponto do forno
img_com_gradiente = adicionar_gradiente(img.copy(), forno_x, forno_y)

# Exibindo a imagem com o círculo de gradiente no Streamlit
st.image(img_com_gradiente, caption="Planta do Forno com Ponto de Localização", use_container_width=True)
