import pygame
import math
import ctypes
import random
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
        self.offset = pygame.math.Vector2(50, 0)
        self.rect.center = (x,y)
        #self.px = 0
        #self.py = 0
        self.angle = 0
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x,rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x))
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    def update(self,vx,vy):
        up,down = 0,height,0,width
        if up < self.rect.y + vy:
            self.rect.y += vy
        if down > self.rect.y +vy:
            self.rect.y += vy
        if self.rect.x + vx > -25:
            self.rect.x += vx
        if self.rect.x + vx < width:
            self.rect.x += vx


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
        vr = 20
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
        im = pygame.image.load("assets/i.png")
        self.image =  pygame.transform.scale(im, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
    def update(self,mapa):
        v_x = self.vx
        v_y = self.vy
        if self.rect.x - mapa.rect.x <= 0:
            v_x = -v_x
            self.vx = v_x
        if self.rect.x - mapa.rect.x >= mapa.rect.w-self.rect.w:
            v_x = -v_x
            self.vx = v_x
        if self.rect.y - mapa.rect.y <= 0:
            v_y = -v_y
            self.vy = v_y
        if self.rect.y - mapa.rect.y >= mapa.rect.h-self.rect.h:
            v_y = -v_y
            self.vy = v_y
        self.rect.x += v_x
        self.rect.y += v_y 
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    #funcao que spawna invasores em packs em lugares aleatorios da tela.
    def spawn(mapa):
        #ponto = (random.randint(0,width),random.randint(0,height))
        ponto = (mapa.rect.x+50,mapa.rect.y+50)
        v_inicial = (random.randint(-5,5),random.randint(-5,5))
        u = invasor(ponto[0],ponto[1],v_inicial[0],v_inicial[1])
        invasores.add(u)

    def dist(self,next):
        distx = (self.rect.x - next.rect.x)**2
        disty = (self.rect.y - next.rect.y)**2
        return math.sqrt(distx + disty)

    #def average_pos_near(self,group):
    #    len_grupo = 0
    #    avgx = 0
    #    avgy = 0
    #    for i in group:
    #        if self.dist(i) <= raio_grupo:
    #            avgx += i.rect.x
    #            avgy += i.rect.y
    #            len_grupo += 1
    #    avgx = avgx/len_grupo
    #    avgy = avgy/len_grupo
    #    return avgx,avgy
    #def steer(self,posx,posy):
    #    ang = math.atan2(posx,posy)
    #    self.vx = -math.cos(ang)*velocidade_unitaria_invasores
    #    self.vy = -math.sin(ang)*velocidade_unitaria_invasores
    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * v_inv
        self.rect.y += dy * v_inv









    
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
all_sprites = pygame.sprite.Group()
