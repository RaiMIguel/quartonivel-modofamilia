import pygame
from constantes import TILE_SIZE, ESCALA_PERSONAGEM, CAMINHO_ASSETS
import os

def carregar_sprites():
    sprites = {
        "cima": pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagemCostas.png")).convert_alpha(),
        "baixo": pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagemFrente.png")).convert_alpha(),
        "direita": pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagemDireito.png")).convert_alpha(),
        "esquerda": pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagemEsquerdo.png")).convert_alpha()
    }

    for direcao in sprites:
        sprites[direcao] = pygame.transform.scale(
            sprites[direcao],
            (int(TILE_SIZE * ESCALA_PERSONAGEM), int(TILE_SIZE * ESCALA_PERSONAGEM))
        )
    
    return sprites

def mover_personagem(teclas, posicao, mapa_colisao):
    x, y = posicao
    nova_x, nova_y = x, y
    direcao = None

    if teclas[pygame.K_UP]:
        nova_y -= 1
        direcao = "cima"
    elif teclas[pygame.K_DOWN]:
        nova_y += 1
        direcao = "baixo"
    elif teclas[pygame.K_LEFT]:
        nova_x -= 1
        direcao = "esquerda"
    elif teclas[pygame.K_RIGHT]:
        nova_x += 1
        direcao = "direita"

    if direcao is None:
        # Nenhuma tecla pressionada: posição e direção permanecem iguais
        return (x, y), None

    # Checa colisão e retorna nova posição/direção válida
    if 0 <= nova_x < len(mapa_colisao[0]) and 0 <= nova_y < len(mapa_colisao):
        if mapa_colisao[nova_y][nova_x] == 1:
            return (nova_x, nova_y), direcao

    # Movimento inválido (colisão), permanece na posição atual
    return (x, y), None
