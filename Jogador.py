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
        self.mapa = mapa

        #Carregando imagens de animação do jogador:
        self.images = [

            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman01.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman02.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman03.png').convert_alpha(), tamanho),
            pygame.transform.scale(pygame.image.load('Bomberman/bomberwoman04.png').convert_alpha(), tamanho)
        ]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

        #Definindo posição inicial do jogador:
        self.rect.topleft = posicao

        #Tempo de troca de animação:
        self.tempo_animacao = 0.01
        self.contador_tempo = 0

        #Variaveis de controle do tempo de plantar a bomba:
        self.tempo_ultimo_plante = 0
        self.intervalo_bomba = 3
     

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

    def movimento(self):
        keys = pygame.key.get_pressed()
        movimento_x = 0
        movimento_y = 0
        if keys[pygame.K_w]:
            movimento_y -= self.__velocidade
            self.image = self.images[2]
        if keys[pygame.K_s]:
            movimento_y += self.__velocidade
            self.image = self.images[0]
        if keys[pygame.K_d]:
            movimento_x += self.__velocidade
            self.image = self.images[1]
        if keys[pygame.K_a]:
            movimento_x -= self.__velocidade
            self.image = self.images[3]
        
   #Movimenta o Jogador no eixo X e checa colisões:
        self.rect.x += movimento_x
        bloco_colidido = pygame.sprite.spritecollideany(self, self.mapa.blocos)  
        bomba_colidida = pygame.sprite.spritecollideany(self, self.mapa.bombas) 
        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='x')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='x')
     
    # Movimenta o jogador no eixo Y e checa colisões
        self.rect.y += movimento_y
        bloco_colidido = pygame.sprite.spritecollideany(self, self.mapa.blocos)  
        bomba_colidida = pygame.sprite.spritecollideany(self, self.mapa.bombas) 
        if bloco_colidido or bomba_colidida:
            if bloco_colidido:
                self.colisao(bloco_colidido, eixo='y')
            if bomba_colidida:
                self.colisao(bomba_colidida, eixo='y')

        self.__posicao = self.rect.topleft

    def colisao(self, sprite, eixo):
        for bomba in self.mapa.bombas:
            if pygame.sprite.collide_rect(self, bomba):
               print("Colisão com bomba detectada")
        if eixo == 'x':
            if self.rect.right > sprite.rect.left and self.rect.left < sprite.rect.right:
                if self.rect.centerx < sprite.rect.centerx:
                   self.rect.right = sprite.rect.left
                else:
                   self.rect.left = sprite.rect.right
        if eixo == 'y':
            if self.rect.bottom > sprite.rect.top and self.rect.top < sprite.rect.bottom:
                if self.rect.centery < sprite.rect.centery:
                   self.rect.bottom = sprite.rect.top
                else:
                   self.rect.top = sprite.rect.bottom


    #Metodo para Jogador plantar a bomba, ajuste de tamanho, tempo, raio da bomba e o tempo de um plante para o outro:
    def plantar_bomba(self, dt):
        current_time = pygame.time.get_ticks() / 1000 #Obtem o tempo atual em segundos
        if current_time - self.tempo_ultimo_plante >= self.intervalo_bomba:
            if self.image == self.images[0]:
                bomba_pos = (self.rect.centerx - 25, (self.rect.bottom + self.rect.height // 2) - 10)
            elif self.image == self.images[1]:  #Imagem apontando para direita
                bomba_pos = ((self.rect.right + self.rect.width // 2) - 20, self.rect.centery - 19)
            elif self.image == self.images[2]:  #Imagem apontando para cima
                bomba_pos = (self.rect.centerx - 20, (self.rect.top - self.rect.height // 2) - 20)
            elif self.image == self.images[3]:  #Imagem apontando para esquerda
                bomba_pos = (self.rect.left - 40, self.rect.centery - 20)
                        
            bomba = Bomba(bomba_pos, 4.0, 50, (40, 40), self.mapa)

            self.mapa.bombas.add(bomba)
            self.tempo_ultimo_plante = current_time #Atualiza o tempo da ultima bomba plantada
    
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
        #self.animacao(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.plantar_bomba(dt)
     