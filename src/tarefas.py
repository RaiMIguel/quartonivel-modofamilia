import pygame
from mapa import TILE_SIZE

# Análisa os pixels das areas interatiavas

def criar_areas_interativas():
    mesa_tiles =  [(x, y) for y in range(15, 18) for x in range(27, 33)]
    Computador_tiles = [(x, y) for y in range(17, 19) for x in range(1, 7)]
    pia_cozinha_tiles = [(x, y) for y in range(17, 20) for x in range(21, 23)]
    cama_personagem_tiles = [(x, y) for y in range(17, 21) for x in range(14, 19)]
    Guarda_Roupa_Pais_tiles = [(x, y) for y in range(1, 4) for x in range (13,18)]
    guarda_roupa_personagem_tiles = [(x, y) for y in range(12, 14) for x in range(1, 7)]
    Fogao_tiles = [(x, y) for y in range(17, 20) for x in range(37, 39)]
    

    return [
        {
            "nome": "mesa",
            "tiles": mesa_tiles,
            "tipo": "task",
            "tasks": {"arrumar": 40}
        },
        {
            "nome": "Guarda Roupa Pais",
            "tiles": Guarda_Roupa_Pais_tiles,
            "tipo": "task",
            "tasks": {"Arrumar Roupas": 20}
        },
        {
            "nome": "Computador",
            "tiles": Computador_tiles,
            "tipo": "recompensa",
            "recompensas": [("1h de tecnologia", 10), ("Saída misteriosa", 100)]
        },
         {
            "nome": "Fogao",
            "tiles":  Fogao_tiles,
            "tipo": "task",
            "tasks": {"Cozinhar": 20}
        },
        {
            "nome": "Cama Personagem",
            "tiles": cama_personagem_tiles,
            "tipo": "task",
            "tasks": {"Arrumar Cama": 20}
        },
        {
            "nome": "Pia Cozinha",
            "tiles": pia_cozinha_tiles,
            "tipo": "task",
            "tasks": {"Lavar Pratos": 20}
        },
        {
            "nome": "Guarda Roupas",
            "tiles": guarda_roupa_personagem_tiles,
            "tipo": "task",
            "tasks": {"Dobrar Roupas": 15}
        },
    ]


#Analisa se vocÊ está perto de uma área interativa

def esta_perto_tile(pos, tiles):
    px, py = pos
    return any(abs(tx - px) <= 1 and abs(ty - py) <= 1 for tx, ty in tiles)

def detectar_area_interativa(pos, areas):
    for area in areas:
        if esta_perto_tile(pos, area["tiles"]):
            return area
    return None

# analisa ações com o teclado

def lidar_com_teclas_area(evento, area, estado_task, Pontuacao):
    if area["tipo"] == "task":
        if evento.key == pygame.K_e:
            if not estado_task["ativa"]:
                estado_task["ativa"] = True
                estado_task["tempo_inicial"] = pygame.time.get_ticks()
                estado_task["atual"] = estado_task["opcoes"][estado_task["index"]]
        elif evento.key in [pygame.K_TAB, pygame.K_s, pygame.K_w]:
            estado_task["index"] = (estado_task["index"] + 1) % len(estado_task["opcoes"])
    
    elif area["tipo"] == "recompensa":
        if evento.key == pygame.K_e:
            nome, custo = area["recompensas"][estado_task["index"]]
            if Pontuacao >= custo:
                Pontuacao -= custo
                return Pontuacao, f"Resgatado '{nome}' por {custo} pontos!"
        elif evento.key in [pygame.K_TAB, pygame.K_s, pygame.K_w]:
            estado_task["index"] = (estado_task["index"] + 1) % len(area["recompensas"])
    
    return Pontuacao, None

#Desenha menu das tasks

def desenhar_area_interativa(tela, fonte, area, estado_task, personagem_pos, Pontuacao):
    pos_tile = area["tiles"][0]
    pos_x = pos_tile[0] * TILE_SIZE
    pos_y = pos_tile[1] * TILE_SIZE

    if area["tipo"] == "task":
        estado_task["index"] = 0
        if not estado_task["ativa"]:
            for i, nome in enumerate(estado_task["opcoes"]):
                texto = nome.capitalize()
                rect = pygame.Rect(pos_x, pos_y + i * 50, 200, 40)
                cor = (255, 255, 0) if i == estado_task["index"] else (255, 255, 255)
                pygame.draw.rect(tela, (30, 30, 30), rect)
                pygame.draw.rect(tela, cor, rect, 2)
                texto_btn = fonte.render(texto, True, (255, 255, 255))
                tela.blit(texto_btn, (rect.x + 10, rect.y + 8))
        else:
            tempo_passado = (pygame.time.get_ticks() - estado_task["tempo_inicial"]) // 1000
            restante = max(0, 5 - tempo_passado)
            cron_rect = pygame.Rect(pos_x, pos_y, 260, 40)
            pygame.draw.rect(tela, (30, 30, 30), cron_rect)
            pygame.draw.rect(tela, (255, 255, 255), cron_rect, 2)
            texto_crono = fonte.render(f"{estado_task['atual'].title()}: {restante}s", True, (255, 255, 255))
            tela.blit(texto_crono, (cron_rect.x + 10, cron_rect.y + 8))
            if restante <= 0:
                pontos = area["tasks"][estado_task["atual"]]
                return Pontuacao + pontos, f"Você concluiu '{estado_task['atual']}' e ganhou {pontos} pontos"
    
    elif area["tipo"] == "recompensa":
        for i, (nome, custo) in enumerate(area["recompensas"]):
            rect = pygame.Rect(pos_x, pos_y + i * 50, 280, 40)
            cor = (255, 255, 0) if i == estado_task["index"] else (255, 255, 255)
            pygame.draw.rect(tela, (30, 30, 30), rect)
            pygame.draw.rect(tela, cor, rect, 2)
            texto_rec = fonte.render(f"{nome} - {custo} pts", True, (255, 255, 255))
            tela.blit(texto_rec, (rect.x + 10, rect.y + 8))

    return Pontuacao, None


# Tasks Quintal

def criar_areas_interativas_Quintal():
    Pets_tiles =  [(x, y) for x in range(2, 8) for y in range(8,10)]
    Horta_tiles =  [(x, y) for x in range(17, 39) for y in range(0, 2)] 

    Carro_tiles =  [(x, y) for x in range(7, 16) for y in range(16, 19)] 

    Carro2_tiles =  [(x, y) for x in range(24, 33) for y in range(16, 19)]
    

    return [
        {
            "nome": "Pets",
            "tiles": Pets_tiles,
            "tipo": "task",
            "tasks": {"Brincar": 5}
        },
          {
            "nome": "Horta",
            "tiles": Horta_tiles,
            "tipo": "task",
            "tasks": {"Regar as Plantas": 15}
        },
          {
            "nome": "Carro",
            "tiles": Carro_tiles,
            "tipo": "task",
            "tasks": {"Lavar Carro": 20}
        },
          {
            "nome": "Carro2",
            "tiles": Carro2_tiles,
            "tipo": "task",
            "tasks": {"Clonar Placa": 1000}
        },
    ]


#Analisa se vocÊ está perto de uma área interativa

def esta_perto_tile_Quintal(pos, tiles):
    px, py = pos
    return any(abs(tx - px) <= 1 and abs(ty - py) <= 1 for tx, ty in tiles)

def detectar_area_interativa_Quintal(pos, areas):
    for area in areas:
        if esta_perto_tile_Quintal(pos, area["tiles"]):
            return area
    return None

# analisa ações com o teclado

def lidar_com_teclas_area_Quintal(evento, area, estado_task, Pontuacao):
    if area["tipo"] == "task":
        if evento.key == pygame.K_e:
            if not estado_task["ativa"]:
                estado_task["ativa"] = True
                estado_task["tempo_inicial"] = pygame.time.get_ticks()
                estado_task["atual"] = estado_task["opcoes"][estado_task["index"]]
        elif evento.key in [pygame.K_TAB, pygame.K_s, pygame.K_w]:
            estado_task["index"] = (estado_task["index"] + 1) % len(estado_task["opcoes"])
    
    elif area["tipo"] == "recompensa":
        if evento.key == pygame.K_e:
            nome, custo = area["recompensas"][estado_task["index"]]
            if Pontuacao >= custo:
                Pontuacao -= custo
                return Pontuacao, f"Resgatado '{nome}' por {custo} pontos!"
        elif evento.key in [pygame.K_TAB, pygame.K_w, pygame.K_s]:
            estado_task["index"] = (estado_task["index"] + 1) % len(area["recompensas"])
    
    return Pontuacao, None

#Desenha menu das tasks

def desenhar_area_interativa_Quintal(tela, fonte, area, estado_task, personagem_pos, Pontuacao):
    pos_tile = area["tiles"][0]
    pos_x = pos_tile[0] * TILE_SIZE
    pos_y = pos_tile[1] * TILE_SIZE

    if area["tipo"] == "task":
        if not estado_task["ativa"]:
            for i, nome in enumerate(estado_task["opcoes"]):
                texto = nome.capitalize()
                rect = pygame.Rect(pos_x, pos_y + i * 50, 200, 40)
                cor = (255, 255, 0) if i == estado_task["index"] else (255, 255, 255)
                pygame.draw.rect(tela, (30, 30, 30), rect)
                pygame.draw.rect(tela, cor, rect, 2)
                texto_btn = fonte.render(texto, True, (255, 255, 255))
                tela.blit(texto_btn, (rect.x + 10, rect.y + 8))
        else:
            tempo_passado = (pygame.time.get_ticks() - estado_task["tempo_inicial"]) // 1000
            restante = max(0, 5 - tempo_passado)
            cron_rect = pygame.Rect(pos_x, pos_y, 260, 40)
            pygame.draw.rect(tela, (30, 30, 30), cron_rect)
            pygame.draw.rect(tela, (255, 255, 255), cron_rect, 2)
            texto_crono = fonte.render(f"{estado_task['atual'].title()}: {restante}s", True, (255, 255, 255))
            tela.blit(texto_crono, (cron_rect.x + 10, cron_rect.y + 8))
            if restante <= 0:
                pontos = area["tasks"][estado_task["atual"]]
                return Pontuacao + pontos, f"Você concluiu '{estado_task['atual']}' e ganhou {pontos} pontos"
    
    elif area["tipo"] == "recompensa":
        for i, (nome, custo) in enumerate(area["recompensas"]):
            rect = pygame.Rect(pos_x, pos_y + i * 50, 280, 40)
            cor = (255, 255, 0) if i == estado_task["index"] else (255, 255, 255)
            pygame.draw.rect(tela, (30, 30, 30), rect)
            pygame.draw.rect(tela, cor, rect, 2)
            texto_rec = fonte.render(f"{nome} - {custo} pts", True, (255, 255, 255))
            tela.blit(texto_rec, (rect.x + 10, rect.y + 8))

    return Pontuacao, None