import pygame
import sys

from constantes import ESCALA_LARGURA, ESCALA_ALTURA, TILE_SIZE

from mapa import Mapa, carregar_Menu
from personagem import carregar_sprites, mover_personagem
from interface import Exibir_Menu

pygame.init()
tela = pygame.display.set_mode((ESCALA_LARGURA, ESCALA_ALTURA))
pygame.display.set_caption("Quarto Nível - Modo Família")

game_map = Mapa(tipo_mapa="casa")

menu_img = carregar_Menu()
Exibir_Menu(tela, menu_img)

sprites = carregar_sprites()
personagem_x, personagem_y = 13, 18
direcao_personagem = "baixo"

ultima_posicao_fixa = (personagem_x, personagem_y)

relogio = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    
    nova_posicao, nova_direcao = mover_personagem(teclas, (personagem_x, personagem_y), game_map)

    if nova_posicao != (personagem_x, personagem_y):
        ultima_posicao_fixa = nova_posicao
    personagem_x, personagem_y = nova_posicao
    #Raí: Essa foi a função que usei para descobri a cordenada exata de cada ponto do mapa!
    #print(f"Posição atual: ({personagem_x}, {personagem_y}) | Mapa: {game_map.mapa_atual}")

    if nova_direcao is not None:
        direcao_personagem = nova_direcao

    # Lógica de Transição: Casa para Quintal
    PORTA_CASA_QUINTAL_X_MIN, PORTA_CASA_QUINTAL_X_MAX = 0, 0
    PORTA_CASA_QUINTAL_Y_MIN, PORTA_CASA_QUINTAL_Y_MAX = 8, 13
    ENTRADA_QUINTAL_X, ENTRADA_QUINTAL_Y = 38, 8

    if game_map.mapa_atual == "casa" and \
       PORTA_CASA_QUINTAL_X_MIN <= personagem_x <= PORTA_CASA_QUINTAL_X_MAX and \
       PORTA_CASA_QUINTAL_Y_MIN <= personagem_y <= PORTA_CASA_QUINTAL_Y_MAX:
        
        game_map = Mapa(tipo_mapa="quintal")
        personagem_x, personagem_y = ENTRADA_QUINTAL_X, ENTRADA_QUINTAL_Y
        
    # Lógica de Transição: Quintal para Casa
    # Tentei usar um elif para não abrir outro if, mas deu erro e o jeito foi crirar as duas lógicas em ifs diferentes.
    PORTA_QUINTAL_CASA_X_MIN, PORTA_QUINTAL_CASA_X_MAX = 39, 40
    PORTA_QUINTAL_CASA_Y_MIN, PORTA_QUINTAL_CASA_Y_MAX = 8, 15
    
    ENTRADA_CASA_X, ENTRADA_CASA_Y = 1, 8

    if game_map.mapa_atual == "quintal" and \
       PORTA_QUINTAL_CASA_X_MIN <= personagem_x <= PORTA_QUINTAL_CASA_X_MAX and \
       PORTA_QUINTAL_CASA_Y_MIN <= personagem_y <= PORTA_QUINTAL_CASA_Y_MAX:
        
        game_map = Mapa(tipo_mapa="casa")
        personagem_x, personagem_y = ENTRADA_CASA_X, ENTRADA_CASA_Y
        
    game_map.draw(tela)

    sprite = sprites[direcao_personagem]
    largura_pers = sprite.get_width()
    altura_pers = sprite.get_height()
    pos_x = personagem_x * TILE_SIZE + (TILE_SIZE - largura_pers) // 2
    pos_y = personagem_y * TILE_SIZE + (TILE_SIZE - altura_pers) // 2
    tela.blit(sprite, (pos_x, pos_y))

    pygame.display.update()
    relogio.tick(15)

pygame.quit()
sys.exit()