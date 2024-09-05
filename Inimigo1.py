import math
import pygame
from Bomba import Bomba
from Inimigo import Inimigo

class Inimigo1(Inimigo):  
    def __init__(self, posicao, vida, velocidade, direcao, mapa, tamanho):
        super().__init__(posicao, vida, velocidade, direcao, mapa, tamanho) 
        
        self.__tempo_ultimo_plante = 0
        self.__intervalo_bomba = 3
        self.__minhas_bombas = []
        self.__direcao = 'direita'
        
        
    @property
    def tempo_ultimo_plante(self):
        return self.__tempo_ultimo_plante

    @property
    def intervalo_bomba(self):
        return self.__intervalo_bomba

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

    #Inimigo cria o objeto bomba e faz o plante:
    def plantar_bomba(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.__tempo_ultimo_plante >= self.__intervalo_bomba:
            bomba = Bomba(self.rect.topleft, 2, 30, (40, 40), self.mapa, dono= self)
            self.__minhas_bombas.append(bomba)
            self.mapa.bombas.add(bomba)
            self.__tempo_ultimo_plante = current_time
            
    def movimento(self, posicao_player, dt: float):  # polimorfismo
        posicao_original = self.rect.topleft

        # Calcula a direção para o jogador
        delta_x = posicao_player[0] - self.rect.centerx
        delta_y = posicao_player[1] - self.rect.centery
        distancia = math.hypot(delta_x, delta_y)

        if distancia != 0:
            direcao_x = (delta_x / distancia) * self.velocidade * dt
            direcao_y = (delta_y / distancia) * self.velocidade * dt
        else:
            direcao_x = 0
            direcao_y = 0

        # Atualiza a posição do inimigo
        self.rect.x += direcao_x
        if pygame.sprite.spritecollideany(self, self.mapa.blocos) or pygame.sprite.spritecollideany(self, self.mapa.bombas):
            self.rect.x = posicao_original[0]

        self.rect.y += direcao_y
        if pygame.sprite.spritecollideany(self, self.mapa.blocos) or pygame.sprite.spritecollideany(self, self.mapa.bombas):
            self.rect.y = posicao_original[1]

        # Atualiza a posição interna
        self.__posicao = self.rect.topleft

        # Atualiza a direção da animação
        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                self.__direcao = 'direita'
            else:
                self.__direcao = 'esquerda'
        else:
            if delta_y > 0:
                self.__direcao = 'baixo'
            else:
                self.__direcao = 'cima'

        # Atualiza a imagem do inimigo de acordo com a direção
        self.__image = self.imagens_direcoes[self.__direcao][self.image_index]

        # Verifica se o caminho está bloqueado e planta bomba
        if self.caminho_bloqueado():
            self.plantar_bomba()
        
        
    def colidir_propria_bomba(self):
        for bomba in self.__minhas_bombas:
            if self.rect.colliderect(bomba.rect):
                return True
        return False

    def animacao(self, dt: float):
        # Atualiza o contador de tempo para a animação
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index = (self.image_index + 1) % 3  # Atualiza o índice da imagem (0 a 2)
            self.__image = self.imagens_direcoes[self.__direcao][self.image_index]  # Atualiza a imagem de acordo com a direção

