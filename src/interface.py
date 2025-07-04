import pygame
import sys

def Exibir_Menu(tela,menu_img):

    botoes = [ 
        {"rect": pygame.Rect(340, 410, 600, 85)}
        
    ]
    rodando = True
    while rodando:
        tela.blit(menu_img, (0, 0))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    if botao["rect"].collidepoint(evento.pos):
                        return "em manutenção"  # Retorna a opção escolhida