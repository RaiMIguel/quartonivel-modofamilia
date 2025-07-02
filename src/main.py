import pygame
from constantes import ESCALA_LARGURA, ESCALA_ALTURA
from mapa import carregar_casa, carregar_quintal

pygame.init()
tela = pygame.display.set_mode((ESCALA_LARGURA, ESCALA_ALTURA))
pygame.display.set_caption("Casa com tarefas")

casa_img = carregar_casa()
quintal = carregar_quintal()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.blit(casa_img, (0, 0))
    pygame.display.update()

pygame.quit()
