import pygame
import math

width,height = 1920,1080
HALF_WIDTH,HALF_HEIGHT = int(width/2),int(height/2)

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
    def update(self,v):
        a = pygame.key.get_pressed()[pygame.K_a]
        s = pygame.key.get_pressed()[pygame.K_s]
        d = pygame.key.get_pressed()[pygame.K_d]
        w = pygame.key.get_pressed()[pygame.K_w]
        if a:
            self.rect.x -= v
        if s:
            self.rect.y += v
        if d:
            self.rect.x += v
        if w:
            self.rect.y -= v

    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def draw_hitbox(self,screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x,rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle =  ((180 / math.pi) * -math.atan2(rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, self.angle)


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

class Camera(object):
    def __init__(self, width, height):
        self.state = pygame.Rect(0, 0, width, height)
        
    def apply(self, target):
        return target.rect.move(self.state.topleft)
        
    def update(self, target):
        self.state = self.simple_camera(self.state, target.rect)
    
    def simple_camera(self, camera, target_rect):
        l, t, _, _ = target_rect # l = left,  t = top
        _, _, w, h = camera      # w = width, h = height
        return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)
    


tiros = pygame.sprite.Group()
invasores = pygame.sprite.Group()
players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
