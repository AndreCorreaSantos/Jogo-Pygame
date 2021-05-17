import pygame
from Classes import *
import random
pygame.init()
#mudando informações da janela
pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("cirurgia-robotica.png")
#iniciando tela
screen = pygame.display.set_mode((width,height))
mapa1 = map("u.jpg",0,0)
mapas.add(mapa1)
background = pygame.Surface((width*2,height*2))
pygame.display.set_icon(icon)
p1 = player('player.png',width/2,height/2)
players.add(p1)
#booleana para testar
running = True
#relogios
clock = pygame.time.Clock()
start_t = pygame.time.get_ticks()
start = pygame.time.get_ticks()
start_w = pygame.time.get_ticks()
start_r = pygame.time.get_ticks()
for i in range(10):
    x_aleatorio = random.randint(0,width)
    y_aleatorio = random.randint(0,height-180)
    u = invasor(x_aleatorio,y_aleatorio)
    all_sprites.add(u)
    invasores.add(u)

while running: 
    clock.tick(120)
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    m1 = pygame.mouse.get_pressed()[0]
    m2 = pygame.mouse.get_pressed()[2]
    m3 = pygame.mouse.get_pressed()[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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

    vx,vy = camera_update(p1,5)

    tiros.update()
    invasores.update(0,0)

    col = pygame.sprite.groupcollide(tiros,invasores,True,True)

    for i in col:
        x_aleatorio = random.randint(0,width)
        y_aleatorio = random.randint(0,height-420)
        i = invasor(x_aleatorio,y_aleatorio)
        all_sprites.add(i)
        invasores.add(i)

    mapa1.rect.x += vx
    mapa1.rect.y += vy
    mapa1.draw(screen)

    for i in all_sprites:
        i.rect.x += vx
        i.rect.y += vy
        i.draw(screen)
    
    
    p1.rotate()
    p1.draw(screen)
    #draw_hb(all_sprites,screen)
    #p1.draw_hitbox(screen)


    pygame.display.update()
