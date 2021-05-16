import pygame
from Classes import *
import random

pygame.init()


screen = pygame.display.set_mode((width,height))

background = pygame.image.load("u.jpg")

pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("cirurgia-robotica.png")
pygame.display.set_icon(icon)




p1 = player('player.png',width/2,height/2) 
players.add(p1)

running = True

clock = pygame.time.Clock()
all_sprites.add(p1)




start_t = pygame.time.get_ticks()
start = pygame.time.get_ticks()
start_w = pygame.time.get_ticks()
start_r = pygame.time.get_ticks()
# instanciando camera
camera = Camera(width,height)

while running: 
    screen.blit(background,(0,0))
    clock.tick(120)


    #for sprite in all_sprites:
    # sprite.draw_hitbox(screen)

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

    p1.update(5)
    camera.update(p1)

    tiros.update()
    invasores.update(0,0)

    col = pygame.sprite.groupcollide(tiros,invasores,True,True)
    for i in col:
        x_aleatorio = random.randint(0,width)
        y_aleatorio = random.randint(0,height-420)
        i = invasor(x_aleatorio,y_aleatorio)
        all_sprites.add(i)
        invasores.add(i)
    
    for i in all_sprites:
        i.rect.x = camera.apply(i).x
        i.rect.y = camera.apply(i).y
        screen.blit(i.image, camera.apply(i))

    pygame.display.update()
