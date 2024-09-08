import pygame
import sys
from Mapa import Mapa
from Jogador import Player
from Inimigo import Inimigo
from InimigoY import InimigoY
from InimigoX import InimigoX
from Inimigo1 import Inimigo1
from tkinter import *


pygame.init()
#Ajusta o tamanho da tela de acordo com o monitor do usuário
root = Tk()
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

num_blocos_x = 15
num_blocos_y = 15
tamanho_bloco = (monitor_height // num_blocos_y) - 5

largura = num_blocos_x * tamanho_bloco
altura =  num_blocos_y * tamanho_bloco

largura_info = 200  #Largura da área de informações
largura_total = largura + largura_info

tela = pygame.display.set_mode((largura_total, altura), pygame.RESIZABLE)

pygame.display.set_caption("Bomberwoman") #

preto = (0,0,0)
branco = (255,255,255)

def game_over_d(tela):
    game_over_imagem = pygame.image.load("telas/Tela_Game_Overr.png")
    game_over_imagem = pygame.transform.scale(game_over_imagem,(largura, altura))
    tela.blit(game_over_imagem, (0,0))
    pygame.display.flip()

def tela_vitoria(tela):
    vitoria_imagem = pygame.image.load("telas/tela_Vitoriaa.png")
    vitoria_imagem = pygame.transform.scale(vitoria_imagem, (largura, altura))
    tela.blit(vitoria_imagem, (0,0))
    pygame.display.flip()
    
def desenhar_informacoes(tela, jogador, tempo, recorde, inimigos_restantes):
    fonte = pygame.font.Font(None, 36)
    texto_vida = fonte.render(f"Vida: {jogador.vida}", True, branco)
    texto_tempo = fonte.render(f"Tempo: {tempo}", True, branco)
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, branco)
    texto_inimigos = fonte.render(f"Inimigos: {inimigos_restantes}", True, branco)

    tela.blit(texto_vida, (largura + 10, 10))
    tela.blit(texto_tempo, (largura + 10, 50))
    tela.blit(texto_recorde, (largura + 10, 90))
    tela.blit(texto_inimigos, (largura + 10, 130))

def main():
    clock = pygame.time.Clock()
    rodando = True
    game_over = False
    vitoria = False

    mapa = Mapa(num_blocos_x, num_blocos_y, tamanho_bloco, tela)
    tamanho_imagem = (tamanho_bloco - 9, tamanho_bloco - 9)
    tamanho_imagem_inimigo = (tamanho_bloco - 9, tamanho_bloco - 9)
    jogador = Player((60, 60), 1, 2, 3, mapa, tamanho= tamanho_imagem)
    inimigo = Inimigo1((tamanho_bloco * 14, tamanho_bloco * 14), 1, 12, 'direcao', mapa, tamanho = tamanho_imagem_inimigo)
    inimigoY = InimigoY((tamanho_bloco * 4, tamanho_bloco * 10), 1, 9, 'direcao', mapa, tamanho = tamanho_imagem_inimigo)
    inimigoX = InimigoX((tamanho_bloco * 14, tamanho_bloco * 2), 1, 9, 'direcao', mapa, tamanho = tamanho_imagem_inimigo)
    
    mapa.jogadores = [jogador]
    mapa.inimigos = [inimigo, inimigoY, inimigoX]
    
    pontuacao = 0
    #Registrar o tempo de início
    tempo_inicio = pygame.time.get_ticks()

    sprites = pygame.sprite.Group()
    sprites.add(jogador)
    sprites.add(inimigo)
    sprites.add(inimigoY)
    sprites.add(inimigoX)
    
    #Abrir o arquivo para leitura
    with open('recorde.txt', 'r') as arquivo:
        recorde = arquivo.read()  #Lê todo o conteúdo do arquivo
        print(recorde)
        
    if recorde == '':
        recorde = 0 #Tratamento de excessões

    #Inicializa o mixer de som do pygame
    pygame.mixer.init()
    #Carrega a música
    pygame.mixer.music.load('musiquinhawavV2.wav')  # Substitua pelo caminho da sua música
    #Define a música para tocar em loop (-1 significa loop infinito)
    pygame.mixer.music.play(loops=-1)
    
            
    while rodando:
        dt = clock.tick(60) / 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               rodando = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    tempo_inicio = pygame.time.get_ticks()
                    main() #Reinicia o jogo
                elif game_over and event.key == pygame.K_e:
                    rodando = False
                elif vitoria and event.key == pygame.K_r:
                    main() #Reinicia o jogo
                elif vitoria and event.key == pygame.K_e:
                    rodando = False


        if not game_over and not vitoria:       
            
    
            jogador.update(dt)
            inimigo.update(jogador.rect.topleft, dt)
            inimigoY.update(jogador.rect.topleft, dt)
            inimigoX.update(jogador.rect.topleft, dt)

            tela.fill(preto)
            mapa.desenhar(tela)
            if(mapa.bombas.update(dt)):
                jogador.sofrer_dano()
            mapa.bombas.draw(tela)
            sprites.draw(tela)

            #Atualização dos sprites
            mapa.explosoes.update(dt)

            #Desenho dos sprites
            mapa.explosoes.draw(mapa.tela)

            mapa.update(dt)
            
            #Contagem de inimigos vivos
            num_inimigos = sum(1 for inimigo in mapa.inimigos if inimigo.alive())
        
            #Desenho da área de informações
            pygame.draw.rect(tela, preto, (largura, 0, largura_info, altura))
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) / 1000  #Tempo em segundos
            desenhar_informacoes(tela, jogador, round(tempo_decorrido), recorde, num_inimigos)

            pygame.display.flip()
        
            pygame.display.flip()
            if not jogador.alive():
                game_over = True
                pygame.mixer.music.stop()
                jogador.som.stop()
            if not inimigo.alive() and not inimigoY.alive() and not inimigoX.alive():
                pygame.mixer.music.stop()
                jogador.som.stop()
                vitoria = True
                #Calcular a pontuação com base no tempo decorrido
                pontuacao = round(tempo_decorrido)  #Exemplo de cálculo de pontuação
                
                #Desenho da área de informações
                pygame.draw.rect(tela, preto, (largura, 0, largura_info, altura))
                desenhar_informacoes(tela, jogador, pontuacao, recorde, num_inimigos)
                if int(pontuacao) < recorde or recorde == 0:
                    with open('recorde.txt', 'w') as arquivo:
                        arquivo.write(str(pontuacao))
                

        elif game_over:
            game_over_d(tela)
            clock.tick(60)
        elif vitoria:
            tela_vitoria(tela)
            clock.tick(60)

    pygame.quit()
    sys.exit()


main()