import math
import pygame
from Bomba import Bomba
from Inimigo import Inimigo

class Inimigo1(Inimigo):  
    def __init__(self, posicao, vida, velocidade, direcao, mapa, tamanho):
        super().__init__(posicao, vida, velocidade, direcao, mapa, tamanho) 
        
        self.tempo_ultimo_plante = 0
        self.intervalo_bomba = 3
        self.minhas_bombas = []
        self.direcao = 'direita'

        
    #Verifica o caminho para ver se está livre:
    def caminho_bloqueado(self):
        for bloco in self.mapa.blocos:
            if bloco.destrutivel and self.rect.colliderect(bloco.rect.inflate(20,20)):
                return True
        return False

    #Inimigo cria o objeto bomba e faz o plante:
    def plantar_bomba(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.tempo_ultimo_plante >= self.intervalo_bomba:
            bomba = Bomba(self.rect.topleft, 2, 30, (40, 40), self.mapa, dono= self)
            self.minhas_bombas.append(bomba)
            self.mapa.bombas.add(bomba)
            self.tempo_ultimo_plante = current_time
            
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
                self.direcao = 'direita'
            else:
                self.direcao = 'esquerda'
        else:
            if delta_y > 0:
                self.direcao = 'baixo'
            else:
                self.direcao = 'cima'

        # Atualiza a imagem do inimigo de acordo com a direção
        self.image = self.imagens_direcoes[self.direcao][self.image_index]

        # Verifica se o caminho está bloqueado e planta bomba
        if self.caminho_bloqueado():
            self.plantar_bomba()
        
        
    def colidir_propria_bomba(self):
        for bomba in self.minhas_bombas:
            if self.rect.colliderect(bomba.rect):
                return True
        return False

    def animacao(self, dt: float):
        # Atualiza o contador de tempo para a animação
        self.contador_tempo += dt
        if self.contador_tempo >= self.tempo_animacao:
            self.contador_tempo = 0
            self.image_index = (self.image_index + 1) % 3  # Atualiza o índice da imagem (0 a 2)
            self.image = self.imagens_direcoes[self.direcao][self.image_index]  # Atualiza a imagem de acordo com a direção

