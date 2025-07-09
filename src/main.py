import pygame
import pygame

from constantes import ESCALA_LARGURA, ESCALA_ALTURA, TILE_SIZE
from mapa import carregar_casa, carregar_quintal, carregar_Menu
from personagem import carregar_sprites, mover_personagem
from interface import Exibir_Menu


pygame.init()
tela = pygame.display.set_mode((ESCALA_LARGURA, ESCALA_ALTURA))
pygame.display.set_caption("Quarto Nível - Modo Família")


menu_img = carregar_Menu()
Exibir_Menu(tela,menu_img)
casa_img = carregar_casa()
sprites = carregar_sprites()

COLS, ROWS = ESCALA_LARGURA // TILE_SIZE, ESCALA_ALTURA // TILE_SIZE
mapa_colisao = [[1] * COLS for _ in range(ROWS)]

personagem_x, personagem_y = 2, 2
direcao_personagem = "baixo"  # Direção inicial

ultima_posicao_fixa = (personagem_x, personagem_y)

relogio = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    nova_posicao, nova_direcao = mover_personagem(teclas, (personagem_x, personagem_y), mapa_colisao)

    # Atualiza posição
    if nova_posicao != (personagem_x, personagem_y):
        ultima_posicao_fixa = nova_posicao
    personagem_x, personagem_y = nova_posicao

    # Atualiza direção só se nova_direcao não for None
    if nova_direcao is not None:
        direcao_personagem = nova_direcao

    # Desenha fundo
    tela.blit(casa_img, (0, 0))

    # Desenha personagem
    sprite = sprites[direcao_personagem]
    largura_pers = sprite.get_width()
    altura_pers = sprite.get_height()
    pos_x = personagem_x * TILE_SIZE + (TILE_SIZE - largura_pers) // 2
    pos_y = personagem_y * TILE_SIZE + (TILE_SIZE - altura_pers) // 2
    tela.blit(sprite, (pos_x, pos_y))

    pygame.display.update()
    relogio.tick(15)

pygame.quit()
