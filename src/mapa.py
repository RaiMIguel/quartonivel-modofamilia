import pygame
from constantes import CAMINHO_CASA, ESCALA_LARGURA, ESCALA_ALTURA, CAMINHO_QUINTAL

def carregar_casa():
    casa_img = pygame.image.load(CAMINHO_CASA).convert()
    casa_img = pygame.transform.scale(casa_img, (ESCALA_LARGURA, ESCALA_ALTURA))
    return casa_img
def carregar_quintal():
    quintal_img = pygame.image.load(CAMINHO_QUINTAL).convert()
    quintal_img = pygame.transform.scale(quintal_img, (ESCALA_LARGURA, ESCALA_ALTURA))
    return quintal_img

