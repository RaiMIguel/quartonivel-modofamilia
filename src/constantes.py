import os

#Configurações de tela
ESCALA_LARGURA = 1280
ESCALA_ALTURA = 704
TILE_SIZE = 32
ESCALA_PERSONAGEM = 2.5

# === Cálculos derivados ===
COLS = ESCALA_LARGURA // TILE_SIZE
ROWS = ESCALA_ALTURA // TILE_SIZE

# === Caminhos ===
CAMINHO_PASTA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
CAMINHO_CASA = os.path.join(CAMINHO_PASTA, "mapaCasa.png")
CAMINHO_QUINTAL = os.path.join(CAMINHO_PASTA, "mapaQuintal.png")