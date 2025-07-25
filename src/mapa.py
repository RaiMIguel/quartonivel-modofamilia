import pygame
from constantes import CAMINHO_CASA, ESCALA_LARGURA, ESCALA_ALTURA, CAMINHO_QUINTAL, CAMINHO_MENU, TILE_SIZE, COLS, ROWS

def carregar_casa():
    casa_img = pygame.image.load(CAMINHO_CASA).convert()
    casa_img = pygame.transform.scale(casa_img, (ESCALA_LARGURA, ESCALA_ALTURA))
    return casa_img

def carregar_quintal():
    quintal_img = pygame.image.load(CAMINHO_QUINTAL).convert()
    quintal_img = pygame.transform.scale(quintal_img, (ESCALA_LARGURA, ESCALA_ALTURA))
    return quintal_img

def carregar_Menu():
    menu_img = pygame.image.load(CAMINHO_MENU).convert()
    menu_img = pygame.transform.scale(menu_img,(ESCALA_LARGURA, ESCALA_ALTURA))
    return menu_img

class Mapa:
    def __init__(self, tipo_mapa="casa"):
        self.mapa_atual = tipo_mapa
        self.tile_size = TILE_SIZE
        self.cols = COLS
        self.rows = ROWS
        self.background_img = None

        self.areas_livres = []
        self.areas_interativas = {}

        self.mapa_colisão = [[1] * self.cols for _ in range(self.rows)]

        self._load_map_data(tipo_mapa)
        self._build_collision_matrix()

    def _load_map_data(self, tipo_mapa):
        if tipo_mapa == "casa":
            self.background_img = self._carregar_imagem_interna(CAMINHO_CASA)

            self.areas_livres = [] # Váriavel de áreas que não são bloqueadas.
            self.areas_interativas = {} # Váriavel para as áreas que vão ser interativas.

            self.areas_livres += [(x, y) for y in range(5, 6) for x in range(1, 9)] #corredor em baixo cama
            self.areas_livres += [(x, y) for y in range(1, 6) for x in range(9, 19)] #ao lado da cama
            self.areas_livres += [(x, y) for y in range(5, 8) for x in range(10, 13)] #porta quarto pais
            self.areas_livres += [(x, y) for y in range(8, 10) for x in range(1, 21)] # corredor quartos, 
            self.areas_livres += [(x, y) for y in range(8, 9) for x in range(0, 3)] # porta quintal
            self.areas_livres += [(x, y) for y in range(8, 12) for x in range(21, 31)] #corredor cozinha,sala
            self.areas_livres += [(x, y) for y in range(11, 14) for x in range(25, 27)] #porta cozinha
            self.areas_livres += [(x, y) for y in range(14, 20) for x in range(21, 39)] #cozinha 
            self.areas_livres += [(x, y) for y in range(9, 12) for x in range(13, 15)]  #porta quart filho
            self.areas_livres += [(x, y) for y in range(12, 21) for x in range(1, 19)] #quarto

            self.areas_interativas["mesa"] = [(x, y) for y in range(15, 18) for x in range(27, 33)]
            self.areas_interativas["comoda"] = [(x, y) for y in range(0, 0) for x in range(0, 0)]
            self.areas_interativas["guarda_roupa_pais"] = [(x, y) for y in range(1, 4) for x in range (13,18)]
            self.areas_interativas["geladeira"] = [(x, y) for y in range(14, 16) for x in range(37, 39)]
            self.areas_interativas["fogao"] = [(x, y) for y in range(17, 20) for x in range(37, 39)]
            self.areas_interativas["pia_cozinha"] = [(x, y) for y in range(17, 20) for x in range(21, 23)]
            self.areas_interativas["cama_personagem"] = [(x, y) for y in range(17, 21) for x in range(14, 19)]
            self.areas_interativas["computador"] = [(x, y) for y in range(17, 19) for x in range(1, 7)]
            self.areas_interativas["guarda_roupa_personagem"] = [(x, y) for y in range(12, 14) for x in range(1, 7)]

            temp_passable_set = set(self.areas_livres)
            for tile in self.areas_interativas["mesa"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["computador"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["cama_personagem"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["guarda_roupa_personagem"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["comoda"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["guarda_roupa_pais"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["pia_cozinha"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["fogao"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["geladeira"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            self.areas_livres = list(temp_passable_set)

        elif tipo_mapa == "quintal":
            self.background_img = self._carregar_imagem_interna(CAMINHO_QUINTAL)
            
            self.areas_livres = []
            self.areas_interativas = {}

            self.areas_livres += [(x, y) for y in range(0, 21) for x in range(0, 39)] # quital
            self.areas_livres += [(x, y) for y in range(7, 9) for x in range(39, 40)] # porta quital

            self.areas_interativas["porta_quintal_saida"] = [(x, y) for x in range(39, 40) for y in range(7, 9)]
            self.areas_interativas["horta"] = [(x, y) for x in range(17, 39) for y in range(0, 2)] 
            self.areas_interativas["pets"] = [(x, y) for x in range(2, 8) for y in range(8,10)] 
            self.areas_interativas["carro_um"] = [(x, y) for x in range(7, 16) for y in range(16, 19)] 
            self.areas_interativas["carro_dois"] = [(x, y) for x in range(24, 33) for y in range(16, 19)] 

            temp_passable_set = set(self.areas_livres)
            for tile in self.areas_interativas["horta"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["pets"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["carro_um"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)
            for tile in self.areas_interativas["carro_dois"]:
                if tile in temp_passable_set:
                    temp_passable_set.remove(tile)

            self.areas_livres = list(temp_passable_set)

        elif tipo_mapa == "menu":
            self.background_img = self._carregar_imagem_interna(CAMINHO_MENU)
            self.areas_livres = []
            self.areas_interativas = {}
        else:
            print(f"Tipo de mapa desconhecido: {tipo_mapa}")

    def _carregar_imagem_interna(self, caminho_imagem):
        img = pygame.image.load(caminho_imagem).convert()
        img = pygame.transform.scale(img, (ESCALA_LARGURA, ESCALA_ALTURA))
        return img

    def _build_collision_matrix(self):
        self.mapa_colisão = [[1] * self.cols for _ in range(self.rows)]
        for x, y in self.areas_livres:
            if 0 <= x < self.cols and 0 <= y < self.rows:
                self.mapa_colisão[y][x] = 0

    def is_tile_passable(self, tile_x, tile_y):
        if 0 <= tile_x < self.cols and 0 <= tile_y < self.rows:
            return self.mapa_colisão[tile_y][tile_x] == 0
        return False

    def is_near_interactive_area(self, player_tile_x, player_tile_y, area_name, radius=1):
        if area_name not in self.areas_interativas:
            return False
        target_tiles = self.areas_interativas[area_name]
        for tx, ty in target_tiles:
            if abs(tx - player_tile_x) <= radius and abs(ty - player_tile_y) <= radius:
                return True
        return False

    def draw(self, surface):
        if self.background_img:
            surface.blit(self.background_img, (0, 0))