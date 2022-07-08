import pygame
import os
import time

'''def testa_pygame(): #Testa se o PyGame foi inicializado com sucesso
    teste = pygame.init()
    if teste[1] > 0:
        print("Houve um erro na inicialização do PyGame!")
        quit()'''

def importa_imagem(nome_imagem): #Carrega as imagens
    nomecompleto = os.path.join("C:/Users/letic/OneDrive/Documentos/Space_X_cc/imagens/", nome_imagem)
    imagem = pygame.image.load(nomecompleto)
    return imagem

class player():
    pos_x = 30
    pos_y = 245
    spaceship = pygame.transform.scale(importa_imagem('spaceship.png'), (150, 55))
    speed = 3 # Se 2 \/ se -2 /\
    jump = pos_y + 100

def main(): # Inicia o Jogo
    FPS = pygame.time.Clock() # Define o limite do FPS
    player_front = player() # Chama a classe player
    quit_game = False # Define a saída do jogo
    width_bg = 693 # Largura da tela de fundo
    height_bg = 490 # Altura da tela de fundo
    backgroud = pygame.display.set_mode((width_bg, height_bg)) # Define as dimenções da tela
    pygame.display.set_caption("Space X - CC") # Define o título da janela 

    while quit_game == False:

        for event in pygame.event.get(): # Responsável por fechar o jogo

            if event.type == pygame.QUIT:
                quit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_front.speed = -1 * player_front.speed 

        ### Promove o movimento do cenário
        width_bg -= 1
        if width_bg == 1:
            width_bg = 693

        ### Faz o Player saltar
        player_front.pos_y += player_front.speed

        print(player_front.pos_y)
        ### Carrega as imagens na tela
        backgroud.blit(importa_imagem("backgroud.jpg"), ((width_bg-692), 1)) #Backgroud 1
        backgroud.blit(importa_imagem("backgroud.jpg"), (width_bg+1, 1)) #Backgroud 2
        backgroud.blit(player_front.spaceship, (player_front.pos_x, player_front.pos_y)) #Player
        FPS.tick(60) #Limite de FPS
        pygame.display.update() # Atualiza o cenário

main()    