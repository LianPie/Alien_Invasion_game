from typing import Any
import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path= 'graphics/' + color + '.png'
        self.image=pygame.image.load(file_path).convert_alpha()
        self.rect= self.image.get_rect(topleft = (x,y))

        if color == 'purple': self.value= 10
        if color == 'red': self.value= 20
        if color == 'green': self.value= 30
        if color == 'yellow': self.value= 40
    
    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image= pygame.image.load('graphics/extera.png').convert_alpha()
        if side == 'right': 
            x = screen_width+50
            self.speed = -3
        else: 
            x= -50
            self.speed= 3

        self.rect= self.image.get_rect(topleft = (x,60))

    
    def update(self):
        self.rect.x += self.speed