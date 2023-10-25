import pygame 
import sys
from PlayerShip import PLayer
import obstacles
from alien import Alien
from random import choice, randint
from laser import Laser
from alien import Extra

class game:

    def __init__(self):
        #player
        PLayer_sprite= PLayer((screen_weidth/2,screen_height),screen_weidth,5)
        self.ship=pygame.sprite.GroupSingle(PLayer_sprite)
        


        #obstacle
        self.shape = obstacles.shape
        self.block_size= 5
        self.blocks=pygame.sprite.Group()
        self.Obstacle_count= 4
        self.Obstacle_x_pos=  [(num * (screen_weidth/self.Obstacle_count)) for num in range(self.Obstacle_count)]
        self.create_multiple_obstacles(*self.Obstacle_x_pos, x_start=screen_weidth/15, y_start= 480)
        


        #aliens
        self.aliens=pygame.sprite.Group()
        self.alien_lasers= pygame.sprite.Group()
        self.AlienSetup(6, 8)
        self.alienspeed = 1

        #extra
        self.extra=pygame.sprite.GroupSingle()
        self.extra_spawn_time= randint(40,80)

        

    def AlienSetup (self, rows, cols,x_distance=50,y_distance=50, x_offset=100, y_offset=100):
        
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x=  col_index * x_distance + x_offset
                y=  row_index * y_distance + y_offset

                RowColor=''
                if row_index == 0:  RowColor= 'yellow'
                elif 1<= row_index <= 2:    RowColor = 'green'
                elif 3 <= row_index <= 4:   RowColor= 'red'
                else:   RowColor= 'purple'
                
                alien_sprite= Alien(RowColor,x,y)
                self.aliens.add(alien_sprite)

    def alien_move_down(self, distance):
        if self.aliens:
            for Alien in self.aliens.sprites():
                Alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien= choice(self.aliens.sprites())
            laser_sprite= Laser(random_alien.rect.center,screen_height,'white', 6 )
            self.alien_lasers.add(laser_sprite)

    def AlienConstrainte(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_weidth:
                self.alienspeed= -1
            elif alien.rect.left == 0:
                self.alienspeed= 1
                

    def extra_alien_timer(self):
        self.extra_spawn_time -=1
        if self.extra_spawn_time <=0:
            self.extra.add(Extra(choice(['right','left']), screen_weidth))
            self.extra_spawn_time= randint(400,800)
        

    def CreatObstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col=='x':
                    x= x_start + col_index * self.block_size + offset_x
                    y= y_start + row_index * self.block_size 
                    block= obstacles.Block(self.block_size,(255,25,71),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset, x_start, y_start):
        for x in offset:
            self.CreatObstacle(x_start,y_start,x)

   
    def collision_check(self):
        #player lazers
        if self.ship.sprite.lasers:
            for laser in self.ship.sprite.lasers:
                #obstacle
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                #alien
                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    laser.kill()
                #extra
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
        #alien lazers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #obstacle
                if pygame.sprite.spritecollide(laser,self.blocks,False):
                    laser.kill()
                #player
                if pygame.sprite.spritecollide(laser,self.ship,False):
                    laser.kill()
                    print("ow")
        

    def run(self):
        self.ship.sprite.lasers.draw(screen)
        self.ship.update()
        self.aliens.update(self.alienspeed)
        self.AlienConstrainte()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()

        self.ship.draw(screen)
        
        self.blocks.draw(screen)

        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)

        self.collision_check()




if __name__ == '__main__':
    pygame.init()
    screen_weidth= 600
    screen_height= 600
    screen=pygame.display.set_mode((screen_height,screen_weidth))
    clock = pygame.time.Clock()
    game=game()

    ALIENLAZER = pygame.USEREVENT+1
    pygame.time.set_timer(ALIENLAZER,500)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLAZER:
                game.alien_shoot()
        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
