import pygame
from pygame.sprite import Sprite
from Bloco import Bloco
   
class Mapa():    
    def __init__(self, num_blocos_x, num_blocos_y, tamanho_bloco, tela):
        self.__branco = (255,255,255)
        self.__preto = (0,0,0)
        self.__cinza = (128,128,128)
        self.__azul = (0,0,120)
        self.__tela = tela

        self.__num_blocos_x = num_blocos_x
        self.__num_blocos_y = num_blocos_y
        self.__tamanho_bloco = tamanho_bloco

        
        #Definindo mapa
        self.mapa = [
            #'W' = paredes, 'E' = espaços vazios e 'B' = bloco indestrutível, 'D' = bloco destrutível e 'P' = poder
            "WWWWWWWWWWWWWWW",
            "WEEEDDDDDDDEEEW",
            "WEBEBEBEBEBDBEW",
            "WEDDDDDDPEEDDEW",
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
        self.__poder = pygame.sprite.Group()
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

    @property
    def bombas(self):
        return self.__bombas

    @property
    def explosoes(self):
        return self.__explosoes
    
    @property
    def poder(self):
        return self.__poder
    
    
    
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
                elif bloco == 'D':
                    bloco_destrutivel = Bloco('Blocos/bloco_destrutivel.png', x_pos, y_pos, self.__tamanho_bloco, destrutivel= True)
                    self.blocos.add(bloco_destrutivel)
                elif bloco == 'P':
                    bloco_poder = Bloco('Blocos/poder.png', x_pos, y_pos, self.__tamanho_bloco - 15)
                    bloco_poder.centralizar(x_pos + self.__tamanho_bloco // 2, y_pos + self.__tamanho_bloco // 2)
                    self.poder.add(bloco_poder)
    

    def desenhar(self, tela):
        self.blocos.draw(tela)
        self.__poder.draw(tela)
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
            
    