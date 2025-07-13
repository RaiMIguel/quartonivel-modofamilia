import pygame
import sys

def Exibir_Menu(tela,menu_img):
#Definição e cordenadas dos botões
    botoes = [ 
        {"texto": "Jogar", "rect": pygame.Rect(340, 410, 600, 85)},
        {"texto": "Sair", "rect": pygame.Rect(410, 515, 420, 65)}
            ]
#looping principal Menu
    rodando = True
    while rodando:
        tela.blit(menu_img, (0, 0))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
# Return e identificação do botão escolhido
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                      if botao["rect"].collidepoint(evento.pos):
                        return botao["texto"]  # Retorna a opção escolhida