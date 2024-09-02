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

        self.mapa = mapa
        
        # Carregando imagens inimigo
        self.images = [
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
        
                
        self.imagens_direcoes = {
            'baixo': self.images[0:3],
            'direita': self.images[3:6],
            'cima': self.images[6:9],
            'esquerda': self.images[9:12]
        }

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

        # Definindo posição inicial do inimigo
        self.rect.bottomright = posicao

        # Tempo de troca de animação
        self.tempo_animacao = 1
        self.contador_tempo = 0
   


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
       

    def movimento(self, posicao_player, dt: float):
        pass
    
    
    def sofrer_dano(self, fonte):
        if fonte in self.minhas_bombas:
            return
        self.__vida -= 1
        print(f"Inimigo sofreu dano. Vidas restantes: {self.__vida}")
        if self.__vida <= 0:
            self.morrer()
            
    def matar_jogador(self):
        if not self.vida <= 0:
            for jogador in self.mapa.jogadores:
                if pygame.sprite.collide_rect(self, jogador):
                    jogador.morrer()

    def morrer(self):
        print("O Inimigo morreu!!")
        self.kill()

    #Verifica a colisão do inimigo com blocos e bomba:
    def colisao(self, sprite, eixo):
        if eixo == 'x':
            if self.rect.x < sprite.rect.x:
                self.rect.right = sprite.rect.left
            else:
                self.rect.left = sprite.rect.right
        elif eixo == 'y':
            if self.rect.y < sprite.rect.y:
                self.rect.bottom = sprite.rect.top
            else:
                self.rect.top = sprite.rect.bottom

    def animacao(self, dt: float):
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            
    def update(self, posicao_player, dt: float):
        self.movimento(posicao_player, dt)
        # Atualiza animação quando inimigo se move
        self.animacao(dt)
        if not self.vida <= 0:
            if posicao_player[0] - self.rect.centerx <= 40 and posicao_player[1] - self.rect.centery <= 40:
                self.matar_jogador()
