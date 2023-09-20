import pygame
from laser import Laser

class PLayer(pygame.sprite.Sprite):
    def __init__(self,pos,constrainte,speed):
        super().__init__()
        self.image=pygame.image.load('graphics/Player.png').convert_alpha()
        self.rect= self.image.get_rect(midbottom = pos)
        self.speed= speed
        self.max_x_constrainte= constrainte
        self.ready= True
        self.lasertime=0
        self.laser_cooldown= 600
        
        self.lasers= pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready=False
            self.lasertime=pygame.time.get_ticks()
    
    def recharge(self):
        if not self.ready:
            current_time= pygame.time.get_ticks()
            if current_time - self.lasertime >= self.laser_cooldown:
                self.ready= True

    def constrainte(self):
        if self.rect.left <= 0:
             self.rect.left = 0
        if self.rect.right >= self.max_x_constrainte:
             self.rect.right = self.max_x_constrainte

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,self.rect.bottom))
        

    def update(self):
        self.get_input()
        self.constrainte()
        self.recharge()
        self.lasers.update()
