import pygame, random, os, time

class PLAYER:
    pos_x = 0
    pos_y = 0
    vel = 0.0

def insere_laser(laser, player):
    vetor_laser = []
    vetor_laser.append(player.pos_x+130) #Posição 0, eixo X
    vetor_laser.append(player.pos_y+30) #Posição 1, eixo Y
    vetor_laser.append(pygame.Rect(player.pos_x+130, player.pos_y+30, laser.get_rect()[2], laser.get_rect()[3])) #Posição 2, Retangulo para colisão
    vetor_laser.append(25) #Posição 3, Velocidade em que o Laser se movimenta no eixo X
    return vetor_laser

def insere_asteroide(largura_janela, altura_janela):
    vetor_asteroide = []
    vetor_asteroide.append(largura_janela) #Posição 0, eixo X
    vetor_asteroide.append(random.randint(1, altura_janela)) #Posição,  1 eixo Y
    vetor_asteroide.append(random.randint(5, 15)) #Posição 2, velocidade do asteroide no eixo X
    vetor_asteroide.append(random.randint(-1, 1)) #Posição 3, velocidade do asteroide no eixo Y
    vetor_asteroide.append(pygame.Rect(vetor_asteroide[0], vetor_asteroide[1], 50, 50)) #Posição 4, retangulo para colisão
    return vetor_asteroide

def importa_imagem(name):
    fullname = os.path.join('C:/Users/letic/OneDrive/Documentos/Space_X_cc/space', name)
    imagem = pygame.image.load(fullname)
    return imagem

def importa_som(name):
    fullname = os.path.join('C:/Users/letic/OneDrive/Documentos/Space_X_cc/space/', name)
    som = pygame.mixer.Sound(fullname)
    return som

def desenha_score(largura_janela, altura_janela, score):
    fonte_score = (pygame.font.Font(None, 30))
    texto_score = fonte_score.render('SCORE: ', True, (255, 255, 255))
    score_atual = fonte_score.render(str(score), True, (255, 255, 255))
    janela.blit(texto_score, (5, 5))
    janela.blit(score_atual, (texto_score.get_rect()[2]+texto_score.get_rect()[2], 5))

def reinicia(largura_janela, altura_janela):
    reinicia = True
    while reinicia == True:
        for eventos in pygame.event.get(): #Captura os eventos
            if eventos.type == pygame.QUIT: #Sai do jogo quando receber um evento do tipo QUIT
                pygame.quit()

            #Captura as teclas de movimentação e disparo do jogador
            if eventos.type == pygame.KEYDOWN: #Quando a tecla é pressionada
                if eventos.key == pygame.K_r:
                    return True
                if eventos.key == pygame.K_ESCAPE:
                    pygame.quit()
        
        fonte_titulo = (pygame.font.Font(None, 50))
        texto_inicio = fonte_titulo.render('Para reiniciar o jogo precione "R"', True, (255, 255, 255))
        texto_sai = fonte_titulo.render('Para sair do jogo pressione "ESC"', True, (255, 255, 255))
        janela.blit(texto_inicio, (largura_janela/2-texto_inicio.get_rect()[2]/2, altura_janela/5))
        janela.blit(texto_sai, (largura_janela/2-texto_sai.get_rect()[2]/2, altura_janela-texto_sai.get_rect()[3]))
        pygame.display.update()

def menu(largura_janela, altura_janela):
    inicia_jogo = False
    imagem_fundo = pygame.transform.scale(importa_imagem('nebula.png'), (largura_janela, altura_janela))

    #Caracteristicas da câmera
    velocidade_cam = 5.5 #Velocidade com que as imagens de fundo se movem
    camera = largura_janela 

    while inicia_jogo == False:

        #Realiza o movimento das imagens de fundo            
        camera -= velocidade_cam
        if camera <= 1:
            camera = largura_janela
        janela.blit(imagem_fundo, (camera -(largura_janela+1), 1))
        janela.blit(imagem_fundo, (camera, 1))

        for eventos in pygame.event.get(): #Captura os eventos
            if eventos.type == pygame.QUIT: #Sai do jogo quando receber um evento do tipo QUIT
                pygame.quit()

            #Captura as teclas de movimentação e disparo do jogador
            if eventos.type == pygame.KEYDOWN: #Quando a tecla é pressionada
                if eventos.key == pygame.K_SPACE:
                    return True
                if eventos.key == pygame.K_ESCAPE:
                    pygame.quit()

        fonte_titulo = (pygame.font.Font(None, 50))
        fonte_nomes = (pygame.font.Font(None, 25))
        texto_titulo = fonte_titulo.render("Space X - CC", True, (255, 255, 255))
        texto_inicio = fonte_titulo.render('Para iniciar o jogo pressione "Espaço"', True, (255, 255, 255))
        texto_sai = fonte_titulo.render('Para sair do jogo pressione "ESC"', True, (255, 255, 255))
        texto_nome = fonte_nomes.render('Desenvolvido por Lucas Bitello e Luiz Zanoni', True, (255, 255, 255))
        janela.blit(texto_titulo, (largura_janela/2-texto_titulo.get_rect()[2]/2, altura_janela/20))
        janela.blit(texto_inicio, (largura_janela/2-texto_inicio.get_rect()[2]/2, altura_janela/5))
        janela.blit(texto_sai, (largura_janela/2-texto_sai.get_rect()[2]/2, altura_janela-texto_sai.get_rect()[3]))
        janela.blit(texto_nome, (largura_janela/2-texto_nome.get_rect()[2]/2, altura_janela/2))
        pygame.display.update()

def comeca_jogo(largura_janela, altura_janela, player):
    pygame.init()
    FPS = pygame.time.Clock() #Limita a taxa de atualização da tela
    sair_jogo = False
    teclas = {'sobe': False, 'desce': False} #Teclas para movimentação
    score = 0 #Recebe a pontuação do jogador

    #Carrega as imagens do cenário
    nave = pygame.transform.scale(importa_imagem('nave.png'), (150, 50))
    laser = pygame.transform.scale(importa_imagem('laser.png'), (11, 6))
    imagem_fundo = pygame.transform.scale(importa_imagem('nebula.png'), (largura_janela, altura_janela))
    asteroide = importa_imagem('asteroide.png')
    load_municao = importa_imagem('muni.png')

    #Carrega os sons
    som_laser = importa_som('laser.wav')
    
    iterações = 30 #Limita o surgimento de asteroide
    conta_iterações = 0 #Gera um novo asteroide ao atingir o limite
    diminui_interacoes = 0 #Diminui o numero de iterações ao atingir o limite de 1000

    #Matrizes
    matriz_asteroides = [] #Armazena as posições do asteroide em uma Matriz
    matriz_laser = [] #Armazena os lasers com suas posições e seu Rect em uma matriz
    matriz_municao = []

    #Caracteristicas da câmera e velocidade com que as imagens de fundo se movem
    velocidade_cam = 5
    camera = largura_janela

    fonte_score = (pygame.font.Font(None, 30)) #Fonte para desenhar o SCORE na tela

    municao = 20 #Munição que o player tem para disparar
    conta_municoes = 0 #Contador para gerar o bonus
    while sair_jogo == False:

        #Movimenta as imagens de backgroud
        camera -= velocidade_cam
        if camera <= 1:
            camera = largura_janela

        #Desenha as imagens de fundo e o Jogador na tela
        janela.blit(imagem_fundo, (camera -(largura_janela+1), 1))
        janela.blit(imagem_fundo, (camera, 1))
        janela.blit(nave, (player.pos_x, player.pos_y))

        if conta_municoes > 1000: #Ao aintingir o limite gera um bonus de munição para o jogador
            conta_municoes = 0 #Reinicia o contador
            vet_municao = []
            vet_municao.append(largura_janela) #Posição 0, eixo X
            vet_municao.append(random.randint(1, altura_janela)) #Posição 1, eixo Y
            vet_municao.append(10) #Posição 2, velocidade da municao no eixo X
            vet_municao.append(pygame.Rect(vet_municao[0], vet_municao[1], load_municao.get_rect()[2], load_municao.get_rect()[3])) #Posição 3, retangulo para colisão
            matriz_municao.append(vet_municao) #Adiciona na matriz

        #Desenha o SCORE na tela
        texto_score = fonte_score.render('SCORE: ', True, (255, 255, 255))
        score_atual = fonte_score.render(str(score), True, (255, 255, 255))
        janela.blit(texto_score, (5, 5))
        janela.blit(score_atual, (texto_score.get_rect()[2]+5, 5))

        #Desenha o total de muniçao na tela
        texto_municao = fonte_score.render('MUNIÇÂO: ', True, (255, 255, 255))
        municao_atual = fonte_score.render(str(municao), True, (255, 255, 255))
        janela.blit(texto_municao, (200, 5))
        janela.blit(municao_atual, (200+texto_municao.get_rect()[2], 5))
        
        for eventos in pygame.event.get(): #Captura os eventos
            if eventos.type == pygame.QUIT: #Sai do jogo quando receber um evento do tipo QUIT
                sair_jogo = True

            #Captura as teclas de movimentação e disparo do jogador
            if eventos.type == pygame.KEYDOWN: #Quando a tecla é pressionada
                if eventos.key == pygame.K_w or eventos.key == pygame.K_UP:
                    teclas['sobe'] = True
                if eventos.key == pygame.K_s or eventos.key == pygame.K_DOWN:
                    teclas['desce'] = True

                if municao > 0:
                    if eventos.key == pygame.K_SPACE: #Realiza o disparo quando é pressionado espaço
                        matriz_laser.append(insere_laser(laser, player)) #Chama a função para inserir novos lasers na tela
                        som_laser.play() #Faz o som de disparo
                        municao -= 1 #Remove uma munição

            if eventos.type == pygame.KEYUP:  #Quando a tecla é solta
                if eventos.key == pygame.K_w or eventos.key == pygame.K_UP:
                    teclas['sobe'] = False  
                if eventos.key == pygame.K_s or eventos.key == pygame.K_DOWN:
                    teclas['desce'] = False
        
        #Adiciona os asteroides de maneira aleatória no cenário e conta o SCORE
        conta_iterações += 1
        if conta_iterações == iterações: #Se atingir o limite reinicia a contagem
            conta_iterações = 0
            matriz_asteroides.append(insere_asteroide(largura_janela, altura_janela)) #Adiciona novo asteroide
            diminui_interacoes += 10
            score += 10
            conta_municoes += 10
            if diminui_interacoes > 1000: # Atingiu o limite reinicia a contagem
                if iterações >= 5:
                    iterações -= 1
                    diminui_interacoes = 0
                    velocidade_cam += 0.1
                else:
                    diminui_interacoes = None

        #Move o Persenagem
        player_rect = pygame.Rect(player.pos_x, player.pos_y, nave.get_rect()[2]-20, nave.get_rect()[3]-20) #Cria o retangulo para colisao com os asteroides
        if teclas['sobe'] == True and player.pos_y > 0: 
            player.pos_y -= player.vel
            player_rect.y -= player.vel
        if teclas['desce'] == True and player.pos_y < (altura_janela - 50):
            player.pos_y += player.vel
            player_rect.y += player.vel

        #Faz os disparos aparecerem e os movimenta num eixo X:
        for disparo in range(len(matriz_laser)):
            matriz_laser[disparo][0] += matriz_laser[disparo][3]
            matriz_laser[disparo][2].x += matriz_laser[disparo][3]
            janela.blit(laser, (matriz_laser[disparo][0], matriz_laser[disparo][1]))

        #Faz os asteroides aparecerem e os movimentam num eixo X e eixo Y
        for meteor in range(len(matriz_asteroides)):
            matriz_asteroides[meteor][0] -= matriz_asteroides[meteor][2]
            matriz_asteroides[meteor][1] -= matriz_asteroides[meteor][3]
            matriz_asteroides[meteor][4].x -= matriz_asteroides[meteor][2]
            matriz_asteroides[meteor][4].y -= matriz_asteroides[meteor][3]
            janela.blit(asteroide, (matriz_asteroides[meteor][0], matriz_asteroides[meteor][1]))

        #Desenha o bonus de munição na tela e verifica se houve colisão com a nave
        for muni in matriz_municao:
            muni[0] -= muni[2]
            muni[3].x -= muni[2]
            janela.blit(load_municao, (muni[0], muni[1]))
            if muni[3].colliderect(player_rect): #se colidir jogador recebe bonus e apaga bonus da tela
                matriz_municao.remove(muni)
                municao += 20

        #Verifica se os asteroide colidiram com o laser ou  saíram do cenário
        for asteroide_cena in matriz_asteroides:

            if asteroide_cena[0] < -asteroide.get_rect()[2] or asteroide_cena[1] < -asteroide.get_rect()[3]:
                matriz_asteroides.remove(asteroide_cena)

            elif asteroide_cena[4].colliderect(player_rect):
                fonte_titulo = (pygame.font.Font(None, 48))
                texto_gameover = fonte_titulo.render("GAME OVER", True, (255, 255, 255))
                janela.blit(texto_gameover, [largura_janela/2-texto_gameover.get_rect()[2]/2, altura_janela/2])
                pygame.display.update()
                time.sleep(1)
                sair_jogo = True
            else:
                for disparo in matriz_laser:
                    if disparo[0] > largura_janela:
                        matriz_laser.remove(disparo)
                    else:
                        if disparo[2].colliderect(asteroide_cena[4]):
                            matriz_laser.remove(disparo)
                            matriz_asteroides.remove(asteroide_cena)
                            diminui_interacoes += 100
                            conta_municoes += 100
                            score += 100
                            break

        FPS.tick(25)
        pygame.display.update()

pygame.init()
pygame.mixer.init()
#Define as carecteristicas da tela
largura_janela = 1024
altura_janela = 600
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption('Space CC')

#Define a posição do jogador
player = PLAYER()
player.pos_x = largura_janela / 20
player.pos_y = altura_janela / 2
player.vel = 15

#Chama as funçôes do jogo
fica_jogo = True
if menu(largura_janela, altura_janela) == True:
    while fica_jogo == True:
        comeca_jogo(largura_janela, altura_janela, player)
        fica_jogo = reinicia(largura_janela, altura_janela)
pygame.quit()