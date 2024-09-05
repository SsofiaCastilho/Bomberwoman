import pygame
from pygame.sprite import Sprite
from Mapa import Mapa
from Bomba import Bomba

class Player(Sprite): #herança da classe Sprite
    def __init__(self, posicao, vida, velocidade, range_bomba, mapa, tamanho):
        super().__init__() #Inicialização da Super classe: Sprite através de um metodo construtor
        
        self.__posicao = posicao
        self.__vida = vida
        self.__velocidade = velocidade
        self.__range_bomba = range_bomba
        self.__mapa = mapa

        #Carregando imagens de animação do jogador:
        self.__images = [

            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman04.png').convert_alpha(), tamanho)
        ]
        self.__image_index = 0
        self.__image = self.__images[self.__image_index]
        self.__rect = self.__image.get_rect()

        #Definindo posição inicial do jogador:
        self.__rect.topleft = posicao

        #Tempo de troca de animação:
        self.__tempo_animacao = 0.01
        self.__contador_tempo = 0

        #Variaveis de controle do tempo de plantar a bomba:
        self.__tempo_ultimo_plante = 0
        self.__intervalo_bomba = 3
    
    @property 
    def image(self):
        return self.__image 
    
    @property
    def tempo_animacao(self):
        return self.__tempo_animacao
    
    @property 
    def contador_tempo(self):
        return self.__contador_tempo

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
    def raio(self):
        return self.__range_bomba
    
    @property
    def rect(self):
        return self.__rect
    
    def movimento(self):
        keys = pygame.key.get_pressed()
        movimento_x = 0
        movimento_y = 0
        if keys[pygame.K_w]:
            movimento_y -= self.__velocidade
            self.__image = self.__images[2]
        if keys[pygame.K_s]:
            movimento_y += self.__velocidade
            self.__image = self.__images[0]
        if keys[pygame.K_d]:
            movimento_x += self.__velocidade
            self.__image = self.__images[1]
        if keys[pygame.K_a]:
            movimento_x -= self.__velocidade
            self.__image = self.__images[3]
        
   #Movimenta o Jogador no eixo X e checa colisões:
        self.__rect.x += movimento_x
        bloco_colidido = pygame.sprite.spritecollideany(self, self.__mapa.blocos)  
        bomba_colidida = pygame.sprite.spritecollideany(self, self.__mapa.bombas) 
        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='x')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='x')
     
    # Movimenta o jogador no eixo Y e checa colisões
        self.__rect.y += movimento_y
        bloco_colidido = pygame.sprite.spritecollideany(self, self.__mapa.blocos)  
        bomba_colidida = pygame.sprite.spritecollideany(self, self.__mapa.bombas) 
        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='y')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='y')

        self.__posicao = self.__rect.topleft

    def colisao(self, sprite, eixo):
        for bomba in self.__mapa.bombas:
            if pygame.sprite.collide_rect(self, bomba):
               print("Colisão com bomba detectada")
        if eixo == 'x':
            if self.__rect.right > sprite.rect.left and self.__rect.left < sprite.rect.right:
                if self.__rect.centerx < sprite.rect.centerx:
                   self.__rect.right = sprite.rect.left
                else:
                   self.__rect.left = sprite.rect.right
        if eixo == 'y':
            if self.__rect.bottom > sprite.rect.top and self.__rect.top < sprite.rect.bottom:
                if self.__rect.centery < sprite.rect.centery:
                   self.__rect.bottom = sprite.rect.top
                else:
                   self.__rect.top = sprite.rect.bottom


    #Metodo para Jogador plantar a bomba, ajuste de tamanho, tempo, raio da bomba e o tempo de um plante para o outro:
    def plantar_bomba(self, dt):
        current_time = pygame.time.get_ticks() / 1000 #Obtem o tempo atual em segundos
        if current_time - self.__tempo_ultimo_plante >= self.__intervalo_bomba:
            if self.__image == self.__images[0]:
                bomba_pos = (self.__rect.centerx - 25, (self.__rect.bottom + self.__rect.height // 2) - 10)
            elif self.__image == self.__images[1]:  #Imagem apontando para direita
                bomba_pos = ((self.__rect.right + self.__rect.width // 2) - 20, self.__rect.centery - 19)
            elif self.__image == self.__images[2]:  #Imagem apontando para cima
                bomba_pos = (self.__rect.centerx - 20, (self.__rect.top - self.__rect.height // 2) - 20)
            elif self.__image == self.__images[3]:  #Imagem apontando para esquerda
                bomba_pos = (self.__rect.left - 40, self.__rect.centery - 20)
                        
            bomba = Bomba(bomba_pos, 4.0, 50, (40, 40), self.__mapa)

            self.__mapa.bombas.add(bomba)
            self.__tempo_ultimo_plante = current_time #Atualiza o tempo da ultima bomba plantada
    
    #Metodo para dano sofrido pelo jogador:
    def sofrer_dano(self):
        self.__vida -= 1
        if self.__vida <= 0:
            self.morrer()
 
    def morrer(self):
        print("O jogador morreu!!")
        self.kill()

       
    def update(self, dt):
        self.movimento() 
        #self.__animacao(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.plantar_bomba(dt)
     