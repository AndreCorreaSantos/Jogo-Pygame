import pygame
from Classes import *
import random
pygame.init()
#mudando informações da janela
pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("assets/cirurgia-robotica.png")

#iniciando tela,jogador e mapa
screen = pygame.display.set_mode((width,height))
mapa1 = map("assets/u2.jpg",0,0)
mapas.add(mapa1)
all_sprites.add(mapa1)
background = pygame.Surface((width*2,height*2))
pygame.display.set_icon(icon)
p1 = player('assets/player.png',width/2,height/2)
players.add(p1)

#booleana para poder sair do jogo
running = True

#relogios
clock = pygame.time.Clock()
start_t = pygame.time.get_ticks()
start = pygame.time.get_ticks()
start_w = pygame.time.get_ticks()
start_r = pygame.time.get_ticks()
#criando 10 invasores iniciais em cordenadas aleatorias da tela
for i in range(10):
    x_aleatorio = random.randint(0,width)
    y_aleatorio = random.randint(0,height-180)
    u = invasor(x_aleatorio,y_aleatorio)
    all_sprites.add(u)
    invasores.add(u)

while running: 
    #inicializando clock que cuida do fps
    clock.tick(120)
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    #checando quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #checando eventos criando tiros
    m1 = pygame.mouse.get_pressed()[0]
    m2 = pygame.mouse.get_pressed()[2]
    m3 = pygame.mouse.get_pressed()[1]
    if m1:
        now_w = pygame.time.get_ticks()
        if now_w - start_w >= 200:
            bala = tiro(p1)
            bala.rotate()
            tiros.add(bala)
            all_sprites.add(bala)
            start_w = now_w
    if m2:
        now_t = pygame.time.get_ticks()
        if now_t - start_t >= 200:
            bala2 = tiro(p1)
            bala2.rotate()
            tiros.add(bala2)
            all_sprites.add(bala2)
            start_t = now_t
    #updatando invasore e tiros
    tiros.update()
    invasores.update(0,1)
    #checando colisoes, aplicando colisoes e respawnando invasores
    col = pygame.sprite.groupcollide(tiros,invasores,True,True)
    for i in col:
        x_aleatorio = random.randint(0+vx,width+vx)
        y_aleatorio = random.randint(0,height-420)
        i = invasor(x_aleatorio,y_aleatorio)
        all_sprites.add(i)
        invasores.add(i)
    #recebendo e aplicando os parametros para fazer o offset da camera
    vx,vy = camera_update(5)
    #booleanas para saber se o mapa atingiu limite x ou y do mapa e entao parar de aplicar o offset nas outras entidades.
    testex = True
    testey = True
    for i in all_sprites:
        if type(i) == map:
            testex,testey = i.offset()
            i.rect.x += vx
            i.rect.y += vy
            i.draw(screen)
        else:
            if testex:
                i.rect.x += vx
            if testey:
                i.rect.y += vy
            i.draw(screen)
    #rotacionando jogador na direção do cursor do mouse e blitando ele na tela
    p1.rotate()
    p1.draw(screen)

    #funcao para desenhar a hitbox dos sprites, debug
    #draw_hb(all_sprites,screen)
    #p1.draw_hitbox(screen)
    pygame.display.update()
