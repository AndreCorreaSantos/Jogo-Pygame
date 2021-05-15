import pygame
from funcoes_base import *
import random

pygame.init()


screen = pygame.display.set_mode((width,height))



pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("cirurgia-robotica.png")
pygame.display.set_icon(icon)




p1 = player('player.png',370,480) 
players.add(p1)


p_right = False
p_down = False
p_up = False
p_left = False
w_down = False
e_down = False

running = True

clock = pygame.time.Clock()
all_sprites.add(p1)




start_t = pygame.time.get_ticks()
start = pygame.time.get_ticks()
start_w = pygame.time.get_ticks()
start_r = pygame.time.get_ticks()



while running: 
    screen.fill((255, 230, 250))
    clock.tick(120)


    #for sprite in all_sprites:
    #  sprite.draw_hitbox(screen)

    now = pygame.time.get_ticks()
    if now-start >= 1000:
        x_aleatorio = random.randint(0,width)
        y_aleatorio = random.randint(0,height-180)
        u = invasor(x_aleatorio,y_aleatorio)
        all_sprites.add(u)
        invasores.add(u)
        start = now   


    p1.rotate()


    m1 = pygame.mouse.get_pressed()[0]
    m2 = pygame.mouse.get_pressed()[2]
    m3 = pygame.mouse.get_pressed()[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_a:                        
                p_left = True
            if event.key == pygame.K_d:
                p_right = True
            if event.key == pygame.K_w:
                p_up = True
            if event.key == pygame.K_s:
                p_down = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:              
                p_left = False
            if event.key == pygame.K_d:
                p_right = False
            if event.key == pygame.K_w:
                p_up = False
            if event.key == pygame.K_s:
                p_down = False
    
    velocidade = 5
    x = 0
    y = 0
    if p_left:
        x = -velocidade
    if p_right:
        x = velocidade
    if p_up:
        y = -velocidade
    if p_down:
        y = velocidade
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

    players.update(x,y)
    tiros.update()
    invasores.update(0,random.randint(1,2))


    all_sprites.draw(screen)

    col = pygame.sprite.groupcollide(tiros,invasores,True,True)
    for i in col:
        x_aleatorio = random.randint(0,width)
        y_aleatorio = random.randint(0,height-420)
        i = invasor(x_aleatorio,y_aleatorio)
        all_sprites.add(i)
        invasores.add(i)

    pygame.display.update()
