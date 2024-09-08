import pygame
from pygame.sprite import Sprite
import math
from Explosao import Explosao
    
class Bomba(Sprite): #herança da classe Sprite
    def __init__(self, posicaobomba, tempo, raiodeexplosao, tamanho, mapa, dono = None):
        pygame.sprite.Sprite.__init__(self)

        self.__posicaobomba = posicaobomba
        self.__tempo = tempo
        self.__raiodeexplosao = raiodeexplosao
        self.__tempo_decorrido = 0
        self.__mapa = mapa
        self.__dono = dono
        self.__dano_player = False

        self.__image_index = 0
        
        self.__images = [
            pygame.transform.scale(pygame.image.load('Bombas/bombinha01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bombas/bombinha02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bombas/bombinha03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bombas/bombinha04.png').convert_alpha(), tamanho) 
        ]

        self.__image = self.__images[self.__image_index]
        self.__rect = self.__image.get_rect(topleft = posicaobomba)
        self.__tempo_animacao = 0.3
        self.__contador_tempo = 0
    
    def criar_explosao(self): 
        centro_explosao = (self.__rect.centerx, self.__rect.centery)
        explosao = Explosao(centro_explosao, (self.__raiodeexplosao * 2, self.__raiodeexplosao * 2), 0.3, self.__mapa, dono= self.__dono)

        self.__mapa.explosoes.add(explosao)

        return explosao
    
    def causar_dano(self, explosao):
        raio_explosao = explosao.rect
        bloco_destruido = False

        centro_explosao = raio_explosao.center

        #Identificando o bloco mais proximo do centro da explosão:
        bloco_mais_proximo = None
        menor_distancia = float('inf')

        for bloco in self.__mapa.blocos:
            if bloco.destrutivel:
                bloco_centro = bloco.rect.center
                distancia = math.hypot(bloco_centro[0] - centro_explosao[0], bloco_centro[1] - centro_explosao[1])

                if distancia <= self.__raiodeexplosao + bloco.rect.width / 2:
                    if raio_explosao.colliderect(bloco.rect):
                        if distancia < menor_distancia:
                            menor_distancia = distancia
                            bloco_mais_proximo = bloco
                            print(f"Colisão detectada com bloco destrutível: {bloco.rect}") #Testando a colisão
                            bloco_mais_proximo.kill()
                            self.__mapa.blocos.remove(bloco_mais_proximo)
                            bloco_destruido = True
                        
        for jogador in self.__mapa.jogadores:
            if raio_explosao.colliderect(jogador.rect):
                print("Colisão com jogador detectada")
                self.__dano_player = True

        for inimigo in self.__mapa.inimigos:
            if raio_explosao.colliderect(inimigo.rect):
                if inimigo != self.__dono:
                    print("Colisão com jogador detectada")
                    inimigo.sofrer_dano(self)
                
    
    def explodir(self):
        explosao= self.criar_explosao()
        self.causar_dano(explosao)
        self.kill()


    def update(self, dt):
        dt = dt / 10
        self.__tempo_decorrido +=  dt
        self.__contador_tempo += dt
        if self.__contador_tempo >= self.__tempo_animacao:
            self.__contador_tempo = 0
            self.__image_index = (self.__image_index + 1) % len(self.__images)
            self.__image = self.__images[self.__image_index]
        if self.__tempo_decorrido >= self.__tempo:
            self.explodir()
        if self.__dano_player:
            self.__dano_player = False
            return True
        return False

    
    @property
    def posicaoBomba(self):
        return self.__posicaobomba
    
    @property
    def tempo(self):
        return self.__tempo

    @property
    def raio(self):
        return self.__raiodeexplosao

    @property
    def tempo_decorrido(self):
        return self.__tempo_decorrido

    @property
    def mapa(self):
        return self.__mapa

    @property
    def dono(self):
        return self.__dono

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
    

