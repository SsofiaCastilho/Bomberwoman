import pygame
from pygame.sprite import Sprite


class Explosao(Sprite): #herança da classe Sprite
    def __init__(self, posicao, tamanho, tempo_animacao, mapa, dono = None):
        super().__init__()

        self.__images = [
            pygame.transform.scale(pygame.image.load('Explosão/explosao.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Explosão/explosao2.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Explosão/explosao3.png').convert_alpha(), tamanho)

        ]

        self.__image_index = 0
        self.__image = self.__images[self.__image_index]
        self.__rect = self.__image.get_rect(center = posicao)
        self.__tempo_animacao = tempo_animacao
        self.__contador_tempo = 0
        self.__mapa = mapa
        self.__dono = dono

    def update(self, dt):
        self.__contador_tempo += dt
        if self.__contador_tempo >= self.__tempo_animacao:
            self.__contador_tempo = 0
            self.__image_index += 1
            if self.__image_index < len(self.__images):
                self.__image = self.__images[self.__image_index]
            else:
                self.causar_dano()
                self.kill()
            
    def causar_dano(self):
        for sprite in pygame.sprite.spritecollide(self, self.__mapa.jogadores, False):
            sprite.sofrer_dano() #para diminuir uma vida do jogador
        for sprite in pygame.sprite.spritecollide(self, self.__mapa.inimigos, False):
            if sprite != self.__dono:
                sprite.sofrer_dano(self)



    @property
    def images(self):
        return self.__images

    @property
    def image_index(self):
        return self.__image_index

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def tempo_animacao(self):
        return self.__tempo_animacao

    @property
    def contador_tempo(self):
        return self.__contador_tempo

    @property
    def mapa(self):
        return self.__mapa

    @property
    def dono(self):
        return self.__dono