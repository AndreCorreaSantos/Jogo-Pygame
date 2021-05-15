import pygame
import math

width,height = 800,600

#jogador
class player(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(image)
        self.original_image = pygame.transform.rotate(self.original_image,-90)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.angle = 0
    def update(self,x,y):
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= width-self.rect.width:
            self.rect.x = width -self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= height - self.rect.height:
            self.rect.y = height - self.rect.height
        self.rect.x += x
        self.rect.y += y

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


class tiro(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load("bullet_1.png")
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
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        im = pygame.image.load("i.png")
        self.image =  pygame.transform.scale(im, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,v_x,v_y):
        self.rect.x += v_x
        self.rect.y += v_y
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)


tiros = pygame.sprite.Group()
invasores = pygame.sprite.Group()
players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
