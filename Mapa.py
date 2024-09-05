import pygame
from pygame.sprite import Sprite


class Bloco(Sprite): #herança da classe Sprite
    def __init__(self, imagem, x, y, tamanho_bloco, destrutivel = False):
        super().__init__() #Inicializando a sprite
        self.__image = pygame.image.load(imagem).convert_alpha()
        self.__image = pygame.transform.scale(self.__image,(tamanho_bloco, tamanho_bloco))
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = (x , y) # para definir a posição do retângulo (Bloco destrutivel) na tela
        self.__destrutivel = destrutivel
        self.__jogadores = []
        self.__inimigos = []

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def destrutivel(self):
        return self.__destrutivel

    @property
    def jogadores(self):
        return self.__jogadores

    @property
    def inimigos(self):
        return self.__inimigos
    

    def aumentar_tamanho(self,tamanho_novo):
        center = self.__rect.center
        self.__image = pygame.transform.scale(self.__image,(tamanho_novo, tamanho_novo))
        self.__rect = self.__image.get_rect()
        self.__rect.center = center


    def redimensionar_imagem(self, novo_tamanho):
        self.__image = pygame.transform.scale(self.__image, (novo_tamanho, novo_tamanho))
        self.__rect = self.__image.get_rect(topleft = self.__rect.topleft)

class Mapa:    
    def __init__(self, num_blocos_x, num_blocos_y, tamanho_bloco, tela):
        self.__branco = (255,255,255)
        self.__preto = (0,0,0)
        self.__cinza = (128,128,128)
        self.__azul = (0,0,120)
        self.__tela = tela

        self.__num_blocos_x = num_blocos_x
        self.__num_blocos_y = num_blocos_y
        self.__tamanho_bloco = tamanho_bloco

        
        #definindo mapa
        self.mapa = [
            # 'W' = paredes, 'E' = espaços vazios e 'B' = bloco indestrutível e 'D' = bloco destrutível
            "WWWWWWWWWWWWWWW",
            "WEEEDDDDDDDEEEW",
            "WEBEBEBEBEBDBEW",
            "WEDDDDDDEEEDDEW",
            "WDBEBEBEBEBDBDW",
            "WDDEDDDDDDEDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDDDEEDEDDDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDEDDDDDDDDDDW",
            "WDBEBEBDBEBDBDW",
            "WDDDEEEEDDDDDDW",
            "WEBEBEBEBEBEBEW",
            "WEEEDDDDDDDEEEW",
            "WWWWWWWWWWWWWWW"  

        ]
        

        self.blocos = pygame.sprite.Group()
        self.__bombas = pygame.sprite.Group()
        self.__explosoes = pygame.sprite.Group()
        self.criar_mapa()
        
    @property
    def branco(self):
        return self.__branco

    @property
    def preto(self):
        return self.__preto

    @property
    def cinza(self):
        return self.__cinza

    @property
    def azul(self):
        return self.__azul

    @property
    def tela(self):
        return self.__tela

    @property
    def num_blocos_x(self):
        return self.__num_blocos_x

    @property
    def num_blocos_y(self):
        return self.__num_blocos_y

    @property
    def tamanho_bloco(self):
        return self.__tamanho_bloco

    """@property
    def mapa(self):
        return self.mapa"""

    """@property
    def blocos(self):
        return self.blocos"""

    @property
    def bombas(self):
        return self.__bombas

    @property
    def explosoes(self):
        return self.__explosoes
    
    
    def criar_mapa(self):
        #Desenha os blocos:
        for y, linha in enumerate(self.mapa):
            for x, bloco in enumerate(linha):
                x_pos = x * self.__tamanho_bloco
                y_pos = y * self.__tamanho_bloco
                if bloco == 'W':
                    bloco_lateral = Bloco('Blocos/bloco_lateral.png', x_pos, y_pos, self.__tamanho_bloco)
                    self.blocos.add(bloco_lateral)
                elif bloco == 'B':
                    bloco_fixo = Bloco('Blocos/bloco_estrelas.png', x_pos, y_pos, self.__tamanho_bloco)
                    self.blocos.add(bloco_fixo)
                elif bloco == 'E':
                    bloco_sprite = Bloco('Fundo/fundo.png', x_pos, y_pos, self.__tamanho_bloco)                  
                elif bloco == 'D':
                    bloco_destrutivel = Bloco('Blocos/bloco_destrutivel.png', x_pos, y_pos, self.__tamanho_bloco, destrutivel= True)
                    self.blocos.add(bloco_destrutivel)
    

    def desenhar(self, tela):
        self.blocos.draw(tela)
        self.__bombas.draw(tela)

    def update(self, dt):
        self.__bombas.update(dt)
        
        
    def aumentar_tamanho_bloco(self, novo_tamanho):
        for bloco in self.blocos:
            bloco.aumentar_tamanho(novo_tamanho)

    def obter_blocos_destrutiveis(self):
        for bloco in self.blocos:
            if bloco.destrutivel:
                print(f"Bloco destrutível encontrado: {bloco.rect}")
            
    