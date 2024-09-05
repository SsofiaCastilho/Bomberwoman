from pygame.sprite import Sprite
import pygame
import random
from Mapa import Mapa
from Bomba import Bomba
from Jogador import Player


class Inimigo(Sprite): #herança da classe Sprite
    def __init__(self, posicao, vida, velocidade, direcao, mapa, tamanho):
        super().__init__()
        self.__posicao = posicao
        self.__vida = vida
        self.__velocidade = velocidade
        self.__direcao = direcao
        self.__minhas_bombas = []
        self.__mapa = mapa
        
        # Carregando imagens inimigo
        self.__images = [
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_direita01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_direita02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_direita03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_tras01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_tras02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_tras03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_esquerda01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_esquerda02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load(
                'Inimigo/inimigo_andando_esquerda03.png').convert_alpha(), tamanho)
        ]
        
                
        self.__imagens_direcoes = {
            'baixo': self.__images[0:3],
            'direita': self.__images[3:6],
            'cima': self.__images[6:9],
            'esquerda': self.__images[9:12]
        }

        self.__image_index = 0
        self.__image = self.__images[self.__image_index]
        self.__rect = self.__image.get_rect()

        #Definindo posição inicial do inimigo
        self.__rect.bottomright = posicao

        #Tempo de troca de animação
        self.__tempo_animacao = 1
        self.__contador_tempo = 0
   
    @property
    def minhas_bombas(self):
        return self.__minhas_bombas
    
    @minhas_bombas.setter
    def minhas_bombas(self, bomba):
        self.__minhas_bombas = bomba
        
    @property
    def posicao(self):
        return self.__posicao

    @property
    def vida(self):
        return self.__vida

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def direcao(self):
        return self.__direcao

    @direcao.setter
    def direcao(self, nova_direcao):
        self.__direcao = nova_direcao

    @property
    def mapa(self):
        return self.__mapa

    @property
    def images(self):
        return self.__images

    @property
    def imagens_direcoes(self):
        return self.__imagens_direcoes

    @property
    def image_index(self):
        return self.__image_index
    
    @image_index.setter
    def image_index(self, novo_index):
        self.__image_index = novo_index 

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
    
    @contador_tempo.setter
    def contador_tempo(self, novo_contador):
        self.__contador_tempo = novo_contador

    def movimento(self, posicao_player, dt: float):
        pass
    
    
    def sofrer_dano(self, fonte):
        if fonte in self.__minhas_bombas:
            return
        self.__vida -= 1
        print(f"Inimigo sofreu dano. Vidas restantes: {self.__vida}")
        if self.__vida <= 0:
            self.morrer()
            
    def matar_jogador(self):
        if not self.__vida <= 0:
            for jogador in self.__mapa.jogadores:
                if pygame.sprite.collide_rect(self, jogador):
                    jogador.morrer()

    def morrer(self):
        print("O Inimigo morreu!!")
        self.kill()

    #Verifica a colisão do inimigo com blocos e bomba:
    def colisao(self, sprite, eixo):
        if eixo == 'x':
            if self.__rect.x < sprite.rect.x:
                self.__rect.right = sprite.rect.left
            else:
                self.__rect.left = sprite.rect.right
        elif eixo == 'y':
            if self.__rect.y < sprite.rect.y:
                self.__rect.bottom = sprite.rect.top
            else:
                self.__rect.top = sprite.rect.bottom

    def animacao(self, dt: float):
        self.__contador_tempo += dt
        if self.__contador_tempo >= self.__tempo_animacao:
            self.__contador_tempo = 0
            self.__image_index = (self.__image_index + 1) % len(self.__images)
            self.__image = self.__images[self.__image_index]
            
    def update(self, posicao_player, dt: float):
        self.movimento(posicao_player, dt)
        # Atualiza animação quando inimigo se move
        self.animacao(dt)
        if not self.__vida <= 0:
            if posicao_player[0] - self.__rect.centerx <= 40 and posicao_player[1] - self.__rect.centery <= 40:
                self.matar_jogador()
