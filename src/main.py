import pygame
import sys

from constantes import ESCALA_LARGURA, ESCALA_ALTURA, TILE_SIZE
from tarefas import criar_areas_interativas, detectar_area_interativa, desenhar_area_interativa, lidar_com_teclas_area
from mapa import Mapa, carregar_Menu
from personagem import carregar_sprites, mover_personagem
from interface import Exibir_Menu, desenhar_pontuacao

pygame.init()
tela = pygame.display.set_mode((ESCALA_LARGURA, ESCALA_ALTURA))
pygame.display.set_caption("Quarto Nível - Modo Família")

Pontuacao = 0

game_map = Mapa(tipo_mapa="casa")

menu_img = carregar_Menu()
Exibir_Menu(tela, menu_img)

sprites = carregar_sprites()
personagem_x, personagem_y = 13, 18
direcao_personagem = "baixo"

ultima_posicao_fixa = (personagem_x, personagem_y)

relogio = pygame.time.Clock()
rodando = True

# váriaveis para Execução das Tasks

fonte = pygame.font.SysFont("Arial", 24)
areas = criar_areas_interativas()
estado_task = {
    "ativa": False,
    "tempo_inicial": None,
    "atual": None,
    "opcoes": [],
    "index": 0
}

mensagem_ativa = False
mensagem_texto = ""


# constante iniciar Para começar o Jogo
Iniciar = Exibir_Menu(tela,menu_img)
#Looping Principal agora depende da Opção do Menu
if Iniciar == "Jogar":
    
    while rodando:
        area_atual = detectar_area_interativa((personagem_x, personagem_y), areas)  # MOVER PRA CÁ

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    if mensagem_ativa:
                        mensagem_ativa = False  # Fecha a mensagem
                    elif area_atual:
                        Pontuacao, nova_mensagem = lidar_com_teclas_area(evento, area_atual, estado_task, Pontuacao)
                        if nova_mensagem:
                            mensagem_ativa = True
                            mensagem_texto = nova_mensagem
        

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
        PORTA_QUINTAL_CASA_Y_MIN, PORTA_QUINTAL_CASA_Y_MAX = 7, 9
        
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
        
        desenhar_pontuacao(tela, Pontuacao, posicao=(50, 50))
        
        # Função para detectar de o personagem está perto de uma task

        area_atual = detectar_area_interativa((personagem_x, personagem_y), areas)

# Atualiza opções se estiver perto de uma área nova
        if area_atual and area_atual["tipo"] == "task":
         estado_task["opcoes"] = list(area_atual["tasks"].keys())

# Desenho da área interativa das tasks
        if area_atual and not mensagem_ativa:
            Pontuacao, nova_mensagem = desenhar_area_interativa(tela, fonte, area_atual, estado_task, (personagem_x, personagem_y), Pontuacao)
            if nova_mensagem:
                mensagem_ativa = True
                mensagem_texto = nova_mensagem
                estado_task["ativa"] = False
                estado_task["tempo_inicial"] = None
                estado_task["atual"] = None
                estado_task["index"] = 0
                estado_task["opcoes"] = list(area_atual["tasks"].keys())

        
        pygame.display.update()
        relogio.tick(15)
else:
    pygame.quit()
    sys.exit()