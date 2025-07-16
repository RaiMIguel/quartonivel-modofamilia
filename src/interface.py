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


def desenhar_pontuacao(tela, Pontuacao, posicao=(50, 50)):

#Tamanho e Cor
    Largura_Contador = 200
    Altura_Caixa = 80
    cor_cinza_transparente = (100, 100, 100, 180) 
#Fundo Contador
    caixa = pygame.Surface((Largura_Contador,Altura_Caixa),pygame.SRCALPHA)
#    caixa.fill(cor_cinza_transparente)
    tela.blit(caixa,posicao)
#Texto Posição e Fonte
    Fonte = pygame.font.SysFont("arial",36)
    texto = Fonte.render(f"Pontuação:{Pontuacao}",True,(255,255,255))
    texto_x = posicao[0]+10
    texto_y = posicao[1]+20
    tela.blit(texto,(texto_x,texto_y))