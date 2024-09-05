import math
import pygame
from Inimigo import Inimigo

class InimigoX(Inimigo):  
    def __init__(self, posicao, vida, velocidade, direcao, mapa, tamanho):
        super().__init__(posicao, vida, velocidade, direcao, mapa, tamanho) 
        
        self.__minhas_bombas = []
        self.__direcao = 'esquerda'

    @property
    def minhas_bombas(self):
        return self.__minhas_bombas

    @minhas_bombas.setter
    def minhas_bombas(self, bomba):
        self.__minhas_bombas = bomba
        
    @property
    def direcao(self):
        return self.__direcao

    @direcao.setter
    def direcao(self, nova_direcao):
        self.__direcao = nova_direcao
    
    
    #Verifica o caminho para ver se está livre:
    def caminho_bloqueado(self):
        for bloco in self.mapa.blocos:
            if bloco.destrutivel and self.rect.colliderect(bloco.rect.inflate(20,20)):
                return True
        return False
            
    def movimento(self, posicao_player, dt: float):  # polimorfismo
        posicao_original = self.rect.topleft

        # Decide a direção de movimento do inimigo
        if self.__direcao == 'esquerda':
            self.rect.x -= self.velocidade * dt
        elif self.__direcao == 'direita':
            self.rect.x += self.velocidade * dt

        # Verifica colisão após o movimento no eixo Y
        if pygame.sprite.spritecollideany(self, self.mapa.blocos) or pygame.sprite.spritecollideany(self, self.mapa.bombas):
            # Reverte a direção ao colidir
            self.rect.topleft = posicao_original
            self.__direcao = 'direita' if self.__direcao == 'esquerda' else 'esquerda'

        # Atualiza a imagem do inimigo de acordo com a direção
        self.__image = self.imagens_direcoes[self.__direcao][self.image_index]
        
    def animacao(self, dt: float):
        # Atualiza o contador de tempo para a animação
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index = (self.image_index + 1) % 3  # Atualiza o índice da imagem (0 a 2)
            self.__image = self.imagens_direcoes[self.__direcao][self.image_index]  # Atualiza a imagem de acordo com a direção