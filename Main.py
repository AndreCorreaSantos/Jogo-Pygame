import pygame
from Classes import *
import random
pygame.init()
#mudando informações da janela
pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("assets/cirurgia-robotica.png")

#iniciando tela,jogador e mapa
screen = pygame.display.set_mode((width,height))
mapa1 = map("assets/j.jpg",0,0)
mapa2 = map("assets/u2.jpg",0,0)
mapa3 = map("assets/j2.jpg",0,0)
mapas.add(mapa1)
mapas.add(mapa2)
mapa = mapa1
background = pygame.Surface((width*2,height*2))
pygame.display.set_icon(icon)
p1 = player('assets/player.png',width/2,height/2)
players.add(p1)
all_sprites.add(p1)


#booleana para poder sair do jogo
running = True

#relogios
clock = pygame.time.Clock()
start_t = pygame.time.get_ticks()
start = pygame.time.get_ticks()
start_w = pygame.time.get_ticks()
start_r = pygame.time.get_ticks()
#criando 10 invasores iniciais em cordenadas aleatorias da tela
for i in range(50):
    invasor.spawn(mapa)

conta_kills = 0
click = False
start = False
menu = True
pygame.font.init()
myfont = pygame.font.SysFont("Arial",50)


while running:
    background.fill((0,0,0))
    screen.blit(background,(0,0)) 
    if menu:
        #construindo menu
        button_width = 500
        button_height = 100

        button1_x = width/2-button_width/2
        button1_y = height/2-button_height/2 - 200

        button2_x = button1_x
        button2_y = button1_y + 200

        button3_x = button1_x
        button3_y = button2_y + 200

        text_1 = myfont.render("Start new game",False,(0,0,0))
        text_2 = myfont.render("Load saved game",False,(0,0,0))
        text_3 = myfont.render("options",False,(0,0,0))

        mx,my = pygame.mouse.get_pos()
        button1 = pygame.Rect(button1_x,button1_y,button_width,button_height)
        button2 = pygame.Rect(button2_x,button2_y,button_width,button_height)
        button3 = pygame.Rect(button3_x,button3_y,button_width,button_height)
        if button1.collidepoint((mx,my)):
            if click:
                start = True
                menu = False
        if button2.collidepoint((mx,my)):
            if click:
                dammic = pygame.image.load("assets/x.jpg")
                screen.blit(dammic,(0,0))
        if button3.collidepoint((mx,my)):
            if click:
                pass
        pygame.draw.rect(screen,(75, 0, 130),button1)
        pygame.draw.rect(screen,(75, 0, 130),button2)
        pygame.draw.rect(screen,(75, 0, 130),button3)

        screen.blit(text_1,(button1_x,button1_y))
        screen.blit(text_2,(button2_x,button2_y))
        screen.blit(text_3,(button3_x,button3_y))

    #checando quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    if start == True:
        #checando eventos criando tiros
        m1 = pygame.mouse.get_pressed()[0]
        m2 = pygame.mouse.get_pressed()[2]
        m3 = pygame.mouse.get_pressed()[1]
        if m1:
            now_w = pygame.time.get_ticks()
            if now_w - start_w >= 100:
                bala = tiro(p1)
                bala.rotate()
                tiros.add(bala)
                all_sprites.add(bala)
                start_w = now_w
        if m2:
            now_t = pygame.time.get_ticks()
            if now_t - start_t >= 100:
                bala2 = tiro(p1)
                bala2.rotate()
                tiros.add(bala2)
                all_sprites.add(bala2)
                start_t = now_t
        #updatando invasore e tiros
        for i in invasores:
            i.update(mapa)
        tiros.update()
            #print(i.rect.x)
        #print(len(invasores))
        #checando colisoes, aplicando colisoes e respawnando invasores
        col = pygame.sprite.groupcollide(tiros,invasores,True,True)
        for i in col:
            x_aleatorio = mapa.rect.x+400
            y_aleatorio = mapa.rect.y+400
            i = invasor(x_aleatorio,y_aleatorio,random.randint(-5,5),random.randint(-5,5))
            all_sprites.add(i)
            invasores.add(i)
            conta_kills += 1
        #recebendo e aplicando os parametros para fazer o offset da camera
        velocidade = 6
        scroll = [0,0]
        scroll[0] = int((p1.rect.x-scroll[0]-width/2+p1.rect.w/2)/15)
        scroll[1] = int((p1.rect.y- scroll[1]-height/2+p1.rect.h/2)/15)
        vpx,vpy = camera_update(velocidade)
        #booleanas para saber se o mapa atingiu limite x ou y do mapa e entao parar de aplicar o offset nas outras entidades.
        testex,testey = mapa.offset()
        #mapa.rect.x += vx
        #mapa.rect.y += vy
        mapa.draw(screen)
        scroll[0] = -scroll[0]
        scroll[1] = -scroll[1]
        mapa.rect.x += scroll[0]
        mapa.rect.y += scroll[1]
        for i in all_sprites:
            if type(i) == player:
                i.update(-vpx,-vpy)
                i.rotate()
                if testex:
                    i.rect.x += scroll[0]
                if testey:
                    i.rect.y += scroll[1]
                i.draw(screen)
            elif type(i) == invasor:
                if testex:
                    i.rect.x += scroll[0]
                if testey:
                 i.rect.y += scroll[1]
                i.move_towards_player(p1)
                #i.draw(screen)
                screen.blit(i.image,(i.rect.x+scroll[0],i.rect.y+scroll[1]))
            else:
                if testex:
                    i.rect.x += scroll[0]
                if testey:
                    i.rect.y += scroll[1]
                #i.draw(screen)
                screen.blit(i.image,(i.rect.x+scroll[0],i.rect.y+scroll[1]))
        #troca mapa
        if conta_kills > 50:
            mapa = mapa2
        if conta_kills > 100:
            mapa = mapa3

        textsurface = myfont.render("Kills: {}".format(conta_kills),False,(0,0,0))
        screen.blit(textsurface,(0,0))

        #funcao para desenhar a hitbox dos sprites, debug
        #draw_hb(all_sprites,screen)
        #p1.draw_hitbox(screen)
        #pygame.draw.circle(screen, (0, 0, 0), (width/2, height/2), 10) #--> centro da tela
    pygame.display.update()
