import pygame, random, os
class COLOR:
    vermelho = (255, 0, 0)
    branco = (255, 255, 255)

pygame.init()

#Responsável por definir as dimenções da tela
largura_janela = 800
altura_janela = 600
janela_fundo = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Space X - CC")

def importa_imagem(nome): #Procura imagem e retorna a mesma
    nome_completo = os.path.join("C:/Users/letic/OneDrive/Documentos/Space_X_cc/imagens/", nome)
    imagem = pygame.image.load(nome_completo)
    return imagem

#Inicia a posição no player
velocidade_nave = 5
posicao_nave = [largura_janela/20, altura_janela/2]
rotacao_nave = 0
rect_nave = {'rect': pygame.Rect(posicao_nave[0]-30, posicao_nave[1]-20, 130, 45)}
rect_laser = {'rect': pygame.Rect(posicao_nave[0]+120, posicao_nave[1]+30, 22, 6)}

#Efeito de câmera
mov_camera = largura_janela
vel_camera = 3
FPS = pygame.time.Clock()


#Carrega as imagens
imagem_fundo = pygame.transform.scale(importa_imagem("nebula.png"), (largura_janela, altura_janela))
asteroides = pygame.transform.rotate(importa_imagem("asteroides/Asteroid-A-10-00.png"), 20)
nave = pygame.transform.scale(importa_imagem("spaceship.png"), (150, 50))
laser_red = pygame.transform.scale(importa_imagem("laserred.png"), (22, 6))

#Limita a geração de asteroides
iteracoes = 10
contador = 0
vetor_asteroides = []
vetor_laser = []
sair_jogo = False

color = COLOR()
fonte_titulo = pygame.font.Font(None, 48)
while sair_jogo == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Sair do jogo
            sair_jogo = True

        if event.type == pygame.KEYDOWN: #Dispara laser
            if event.key == pygame.K_SPACE:
                vetor_laser.append({'rect': pygame.Rect(posicao_nave[0]+120, posicao_nave[1]+30, 14, 6), 'pos_x': posicao_nave[0]+120, 'pos_y': posicao_nave[1]+30, 'vel': 10})

    # Sobe, desce, empina e rebola
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        rotacao = 2
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        rotacao = -2
    elif teclas[pygame.K_UP] or teclas[pygame.K_w] and posicao_nave[1] > 0:
        velocidade_nave = -6
    elif teclas[pygame.K_DOWN] or teclas[pygame.K_s] and posicao_nave[1] < altura_janela - 50:
        velocidade_nave = 6
    else:
        rotacao, velocidade_nave = 0, 0

    #Movimenta o jogador no eixo Y e rotaciona
    posicao_nave[1] += velocidade_nave
    rect_nave['rect'].y += velocidade_nave
    rotacao_nave += rotacao

    #Adiciona um novo asteroide
    contador += 1
    if contador > iteracoes:
        pos_x = largura_janela
        pos_y = random.randint(1, altura_janela)
        vel_x = random.randint(3, 10)
        vel_y = random.randint(0, 1)
        contador = 0
        vetor_asteroides.append({'rect': pygame.Rect(pos_x, pos_y+20, 50, 40), 'pos_x': pos_x, 'pos_y': pos_y, 'vel_y': vel_y, 'vel_x': vel_x})

    #Move o cenário
    mov_camera += -vel_camera
    if mov_camera <= 0:
        mov_camera = largura_janela

    #Desenha imagem na tela
    janela_fundo.blit(imagem_fundo, (mov_camera-(largura_janela-1), 1)) #Fundo 1
    janela_fundo.blit(imagem_fundo, (mov_camera+1, 1))                  #Fundo 2
    janela_fundo.blit(pygame.transform.rotate(nave, rotacao_nave), (posicao_nave[0], posicao_nave[1]))         #Nave

    #Verifica colisão com nave
    for asteroide in vetor_asteroides[:]:
        bateu_nave = rect_nave['rect'].colliderect(asteroide['rect'])
        if bateu_nave or asteroide['rect'].x < 0:
            vetor_asteroides.remove(asteroide)
            game_over = True
            sair_jogo = True

    #Desenha asteroides no cenario
    for asteroide in vetor_asteroides:
        asteroide['pos_x'] -= asteroide['vel_x']
        asteroide['rect'].x -= asteroide['vel_x']
        asteroide['pos_y'] -= asteroide['vel_y']
        asteroide['rect'].y -= asteroide['vel_y']
        janela_fundo.blit(asteroides, (asteroide['pos_x'], asteroide['pos_y']))

        #Teste se o asteroide está fora da tela então o exclui da memoria
        if asteroide['pos_x'] < -30:
            vetor_asteroides.remove(asteroide)

    #Desenha o laser na tela
    for laser in vetor_laser:
        laser['pos_x'] += laser['vel']
        laser['rect'].x += laser['vel']
        janela_fundo.blit(laser_red, (laser['pos_x'], laser['pos_y']))
    
    for laser in vetor_laser:
        for asteroide in vetor_asteroides:
            bateu = laser['rect'].colliderect(asteroide['rect'])
            if bateu or asteroide['rect'].x < 0:
                vetor_laser.remove(laser)
                vetor_asteroides.remove(asteroide)
    #Define FPS e atualiza a tela
    FPS.tick(30)
    pygame.display.update()

    while sair_jogo == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Sair do jogo
                sair_jogo = False
        texto_titulo = fonte_titulo.render("GAME OVER", True, color.vermelho, color.branco)
        janela_fundo.blit(texto_titulo, [largura_janela/2, altura_janela/2])
        pygame.display.update()