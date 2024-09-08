import pygame
from pygame.sprite import Sprite

class Bloco(Sprite): #Herança da classe Sprite
    def __init__(self, imagem, x, y, tamanho_bloco, destrutivel = False):
        super().__init__() #Inicializando a sprite
        self.__image = pygame.image.load(imagem).convert_alpha()
        self.__image = pygame.transform.scale(self.__image,(tamanho_bloco, tamanho_bloco))
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = (x , y) #Para definir a posição do retângulo (Bloco destrutivel) na tela
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
    
    def centralizar(self, centro_x, centro_y):
        self.__rect.center = (centro_x, centro_y)

    def aumentar_tamanho(self,tamanho_novo):
        center = self.__rect.center
        self.__image = pygame.transform.scale(self.__image,(tamanho_novo, tamanho_novo))
        self.__rect = self.__image.get_rect()
        self.__rect.center = center


    def redimensionar_imagem(self, novo_tamanho):
        self.__image = pygame.transform.scale(self.__image, (novo_tamanho, novo_tamanho))
        self.__rect = self.__image.get_rect(topleft = self.__rect.topleft)
 