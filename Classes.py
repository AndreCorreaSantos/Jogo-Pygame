import pygame
import math
import ctypes
import random

from pygame import image
user32 = ctypes.windll.user32
width,height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#constantes boid
raio_grupo = 50
v_inv = 5
#jogador
class player(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(image)
        self.original_image = pygame.transform.rotate(self.original_image,-90)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.center = (self.rect.x,self.rect.y)
        self.angle = 0
    def draw(self,screen):
        screen.blit(self.image, (self.rect.center[0]-int(self.image.get_width()/2), self.rect.center[1]-self.image.get_height()/2))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x,rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image,self.angle)
    def update(self,vx,vy):
        if self.rect.x + vx > width -self.rect.w or self.rect.x + vx < 0:
            vx = 0
        if self.rect.y + vy > height-self.rect.h or self.rect.y + vy < 0:
            vy = 0
        self.rect.x += vx
        self.rect.y += vy
        self.pos = (self.rect.x,self.rect.y)

class tiro(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load("assets/bullet_1.png")
        self.original_image =  pygame.transform.scale(im, (30, 30))
        self.original_image = pygame.transform.rotate(self.original_image,-90)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.center[0]
        self.rect.y = player.rect.center[1]
        m_x,m_y = pygame.mouse.get_pos()
        vr = 30
        dx = player.rect.center[0] - m_x
        dy = player.rect.center[1] - m_y
        ang = math.atan2(dy,dx)
        self.vx = -math.cos(ang)*vr
        self.vy = -math.sin(ang)*vr
    def update(self):
        if self.rect.y <= 0 or self.rect.y >= height or self.rect.x <= 0 or self.rect.x >= width:
            self.kill()
        self.rect.x += self.vx
        self.rect.y += self.vy
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x,rel_y = mouse_x - self.rect.center[0], mouse_y - self.rect.center[1]
        self.angle =  ((180 / math.pi) * -math.atan2(rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

class invasor(pygame.sprite.Sprite):
    def __init__(self,x,y,vx,vy):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load("assets/boss.png")
        self.image =  pygame.transform.scale(im, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
        self.vmax = math.sqrt(self.vx**2 + self.vy**2)
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy 
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    #funcao que spawna invasores em packs em lugares aleatorios da tela.
    def spawn(mapa):
        aleatorio = random.randint(1,4)
        if aleatorio == 1:
            aleatorio_x = mapa.rect.x
            aleatorio_y = mapa.rect.y
        elif aleatorio == 2:
            aleatorio_x = mapa.rect.x+mapa.rect.width
            aleatorio_y = mapa.rect.y
        elif aleatorio == 3:
            aleatorio_x = mapa.rect.x
            aleatorio_y = mapa.rect.y + mapa.rect.height
        elif aleatorio == 4:
            aleatorio_x = mapa.rect.x + mapa.rect.width
            aleatorio_y = mapa.rect.y + mapa.rect.height
        v_componente_min = 2
        v_componente_max = 5
        v_aleatoria_x = random.randint(v_componente_min,v_componente_max)
        v_aleatoria_y = random.randint(v_componente_min,v_componente_max)
        u = invasor(aleatorio_x,aleatorio_y,v_aleatoria_x,v_aleatoria_y)
        invasores.add(u)
        all_sprites.add(u)


    def dist(self,next):
        distx = (self.rect.x - next.rect.x)**2
        disty = (self.rect.y - next.rect.y)**2
        return math.sqrt(distx + disty)

    def move_towards_player(self, player):
        dx,dy = self.rect.x - player.rect.x,self.rect.y-player.rect.y
        ang = math.atan2(dy,dx)
        self.vx =  -self.vmax*math.cos(ang)
        self.vy = -self.vmax*math.sin(ang)

class boss(pygame.sprite.Sprite):
    def __init__(self,image,mapa,hp,vx,vy,vmax):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(image).convert_alpha()
        self.image =  pygame.transform.scale(image, (640, 640))
        self.rect = self.image.get_rect()
        self.rect.x = mapa.rect.x + mapa.rect.w/2
        self.rect.y = mapa.rect.y + mapa.rect.h/2
        self.rect.center = (self.rect.x + self.rect.width/2,self.rect.y + self.rect.height/2)
        self.vx = vx
        self.vy = vy
        self.vmax = vmax
        self.hp = hp

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy 

    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)

    def move_towards_player(self, player):
        dx,dy = self.rect.center[0] - player.rect.x, self.rect.center[1] - player.rect.y
        ang = math.atan2(dy,dx)
        self.vx =  -self.vmax*math.cos(ang)
        self.vy = -self.vmax*math.sin(ang)

    
class map(pygame.sprite.Sprite):
    def __init__(self,imagem,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    def offset(self):
        testex = True 
        testey = True
        if self.rect.x >= 0:
            self.rect.x = 0
            testex = False
        if self.rect.x <= width-self.rect.w:
            self.rect.x = width-self.rect.w
            testex = False
        if self.rect.y <= height-self.rect.h:
            self.rect.y = height-self.rect.h
            testey = False
        if self.rect.y >= 0:
            self.rect.y = 0
            testey = False
        return testex,testey
    def update(self,v1,v2):
        self.rect.x += v1
        self.rect.y += v2

def camera_update(velocidade_jogador):
    a = pygame.key.get_pressed()[pygame.K_a]
    s = pygame.key.get_pressed()[pygame.K_s]
    d = pygame.key.get_pressed()[pygame.K_d]
    w = pygame.key.get_pressed()[pygame.K_w]
    vx = 0
    vy = 0
    if a:
        vx = velocidade_jogador
    if s:
        vy = -velocidade_jogador
    if d:
        vx = -velocidade_jogador
    if w:
        vy = velocidade_jogador 
    return vx,vy
def draw_hb(sprites,screen):
    for i in sprites:
        i.draw_hitbox(screen)

tiros = pygame.sprite.Group()
invasores = pygame.sprite.Group()
players = pygame.sprite.Group()
mapas = pygame.sprite.Group()
bosses = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
