import pygame
from Classes import *
import random
pygame.init()
#mudando informações da janela
pygame.display.set_caption("Jogo 1")
icon = pygame.image.load("assets/cirurgia-robotica.png")

#iniciando tela,jogador e mapa
def main():
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
    vidas = 3
    c = 0

    #pygame.mixer.music.load("assets/musica.wav")
    #pygame.mixer.music.play()

    #booleana para poder sair do jogo
    running = True
    options = False
    #relogios
    start = pygame.time.get_ticks()
    start_w = pygame.time.get_ticks()
    relogio = pygame.time.get_ticks()
    #criando 10 invasores iniciais em cordenadas aleatorias da tela



    conta_kills = 0
    start = False
    menu = True
    menu_2 = False
    game_over = False

    pygame.font.init()
    myfont = pygame.font.SysFont("Arial",50)

    #lista de particulas [loc,velocity,timer]
    particles = []
    
    vida = pygame.image.load("assets/vida.png")
    vida = pygame.transform.scale(vida,(64,64))
    v_rect = vida.get_rect().width

    numero_invasores= 10

    while running:
        background.fill((0,0,0))
        screen.blit(background,(0,0)) 

        if menu:
            m1 = pygame.mouse.get_pressed()[0]
            #construindo menu
            button_width = 500
            button_height = 100

            button1_x = width/2-button_width/2
            button1_y = height/2-button_height/2 - 200

            button2_x = button1_x
            button2_y = button1_y + 200

            button3_x = button1_x
            button3_y = button2_y + 200

            if menu_2:
                text_1 = myfont.render("Resume Game",False,(0,0,0))
            else:
                text_1 = myfont.render("Start new Game",False,(0,0,0))

            text_2 = myfont.render("Options",False,(0,0,0))

            if menu_2:
                text_3 = myfont.render("Main menu",False,(0,0,0))
            else:
                text_3 = myfont.render("Quit Game",False,(0,0,0))


            mx,my = pygame.mouse.get_pos()

            button1 = pygame.Rect(button1_x,button1_y,button_width,button_height)
            button2 = pygame.Rect(button2_x,button2_y,button_width,button_height)
            button3 = pygame.Rect(button3_x,button3_y,button_width,button_height)

            if button1.collidepoint((mx,my)):
                if m1:
                    start = True
                    menu = False
                    m1 = False
            if button2.collidepoint((mx,my)):
                if m1:
                    options = True
                    menu = False
                    m1 = False
            if menu_2:
                if button3.collidepoint((mx,my)):
                    relogio2 = pygame.time.get_ticks()
                    tempo = relogio2 - relogio
                    if m1 and tempo > 200:
                        p1.kill()
                        m1 = False
                        relogio = pygame.time.get_ticks()
                        return
            if menu and not menu_2:
                if button3.collidepoint((mx,my)):
                    relogio2 = pygame.time.get_ticks()
                    tempo = relogio2 - relogio
                    if m1 and tempo > 200:
                        pygame.quit()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start = False
                    menu = True
                    menu_2 = True


        if options:
            mouse = pygame.mouse.get_pos()
            apertado = pygame.mouse.get_pressed()[0]

            volume_label_width = 500
            volume_label_height = 100

            volume_label_x = width/2-volume_label_width/2
            volume_label_y = height/2-volume_label_height/2 - 200
            volume_label2_x = volume_label_x
            volume_label2_y = volume_label_y + 200
            return_x = volume_label_x
            return_y = volume_label2_y + 200

            volume_label_rect = pygame.Rect(volume_label_x,volume_label_y,volume_label_width,volume_label_height)
            volume_label2_rect = pygame.Rect(volume_label2_x,volume_label2_y,volume_label_width,volume_label_height)
            return_rect = pygame.Rect(return_x,return_y,volume_label_width,volume_label_height)

            volume_label_text = myfont.render("Sound effects volume",False,(0,0,0))
            volume_label2_text = myfont.render("Music volume",False,(0,0,0))
            return_text = myfont.render("return",False,(0,0,0))

            pygame.draw.rect(screen,(255, 255, 255),volume_label_rect)
            pygame.draw.rect(screen,(255, 255, 255),volume_label2_rect)
            pygame.draw.rect(screen,(75, 0, 130),return_rect)

            screen.blit(volume_label_text,(volume_label_x,volume_label_y))
            screen.blit(volume_label2_text,(volume_label2_x,volume_label2_y))
            screen.blit(return_text,(return_x,return_y))

            if return_rect.collidepoint((mouse)) and apertado:
                relogio = pygame.time.get_ticks()
                options = False
                menu = True



        if start == True:
            #checando eventos criando tiros
            m1 = pygame.mouse.get_pressed()[0]
            if m1:
                now_w = pygame.time.get_ticks()
                if now_w - start_w >= 150:
                    bala = tiro(p1)
                    bala.rotate()
                    tiros.add(bala)
                    all_sprites.add(bala)
                    start_w = now_w
            col = pygame.sprite.groupcollide(tiros,invasores,True,True)
            col2 = pygame.sprite.groupcollide(players,invasores,False,True)
            for i in col:
                for u in range(50):
                    particles.append([[i.rect.x,i.rect.y],[random.randint(0,20)/10 - 1,random.randint(-40,-20)*0.1],random.randint(7,14),random.randint(0,222)])
                u = invasor(random.randint(100,2000),random.randint(100,2000),random.randint(2,5),random.randint(2,5))
                invasores.add(u)
                all_sprites.add(u)

                conta_kills += 1

            for i in col2:
                for u in range(50):
                        particles.append([[i.rect.x,i.rect.y],[random.randint(0,20)/10 - 1,random.randint(-40,-20)*0.1],random.randint(7,14),random.randint(0,222)])

                u = invasor(random.randint(100,2000),random.randint(100,2000),random.randint(2,5),random.randint(2,5))
                invasores.add(u)
                all_sprites.add(u)
                conta_kills += 1
                vidas -= 1
                #tocar animacao de dano
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

            while len(invasores)  < numero_invasores:
                u = invasor(random.randint(100,2000),random.randint(100,2000),random.randint(2,5),random.randint(2,5))
                invasores.add(u)
                all_sprites.add(u)

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
                    i.update(mapa)
                    i.move_towards_player(p1)
                    #i.draw(screen)
                    screen.blit(i.image,(i.rect.x+scroll[0],i.rect.y+scroll[1]))
                else:
                    if testex:
                        i.rect.x += scroll[0]
                    if testey:
                        i.rect.y += scroll[1]
                    i.update()
                    #i.draw(screen)
                    screen.blit(i.image,(i.rect.x+scroll[0],i.rect.y+scroll[1]))

            for particle in particles:
                if testex:
                    particle[0][0] += particle[1][0] + scroll[0]
                else:
                    particle[0][0] += particle[1][0]
                if testey:
                    particle[0][1] += particle[1][1] + scroll[1]
                else:
                    particle[0][1] += particle[1][1]
                particle[2] -= 0.2
                particle[1][1] += 0.1
                c = particle[3]
                pygame.draw.circle(screen, (c,c,c), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    #remove.append(particles.index(particle))
                    particles.remove(particle)

            if conta_kills > 50:
                mapa = mapa2
            if conta_kills > 100:
                mapa = mapa3

            textsurface = myfont.render("Kills: {}".format(conta_kills),False,(0,0,0))
            screen.blit(textsurface,(0,0))

            if not vidas:
                start = False
                game_over = True
            for i in range(vidas):
                screen.blit(vida,(0+i*v_rect,50))
            #funcao para desenhar a hitbox dos sprites, debug
            #draw_hb(all_sprites,screen)
            #p1.draw_hitbox(screen)
            #pygame.draw.circle(screen, (0, 0, 0), (width/2, height/2), 10) #--> centro da tela
            if game_over == True:
                start = False
                menu_2 = False
                p1.kill()

        if game_over:
            mouse = pygame.mouse.get_pos()
            apertado = pygame.mouse.get_pressed()[0]

            game_over_width = 800
            game_over_height = 100

            choice_width = 200
            choice_height = game_over_height

            game_over_x = width/2-game_over_width/2
            game_over_y = height/2-game_over_height/2 - 200

            choice1_x = width/2-(3/2)*choice_width
            choice1_y = height/2-choice_height/2 + 200

            choice2_x = width/2+(1/2)*choice_width
            choice2_y = height/2-choice_height/2 + 200

            game_over_rect = pygame.Rect(game_over_x,game_over_y,game_over_width,game_over_height)
            choice1_rect = pygame.Rect(choice1_x,choice1_y,choice_width,choice_height)
            choice2_rect = pygame.Rect(choice2_x,choice2_y,choice_width,choice_height)

            game_over_text = myfont.render("You died. Do you want to play again?",False,(0,0,0))
            choice1_text = myfont.render("Yes",False,(0,0,0))
            choice2_text = myfont.render("No",False,(0,0,0))

            pygame.draw.rect(screen,(255, 255, 255),game_over_rect)
            pygame.draw.rect(screen,(100, 100, 255),choice1_rect)
            pygame.draw.rect(screen,(255, 100, 100),choice2_rect)

            screen.blit(game_over_text,(game_over_x,game_over_y))
            screen.blit(choice1_text,(choice1_x,choice1_y))
            screen.blit(choice2_text,(choice2_x,choice2_y))

            if choice1_rect.collidepoint(mouse) and apertado:
                return
            if choice2_rect.collidepoint(mouse) and apertado:
                pygame.quit()

        pygame.display.update()

while True:
    main()
