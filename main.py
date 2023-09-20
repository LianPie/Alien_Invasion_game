import pygame 
import sys
from PlayerShip import PLayer
import obstacles
from alien import Alien


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
        self.AlienSetup(6, 8)
        self.alienspeed = 1
        

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

    def AlienConstrainte(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_weidth:
                self.alienspeed= -1
            elif alien.rect.left == 0:
                self.alienspeed= 1
                


    def run(self):
        self.ship.sprite.lasers.draw(screen)
        self.ship.update()
        self.aliens.update(self.alienspeed)
        self.AlienConstrainte()
        

        self.ship.draw(screen)
        
        self.blocks.draw(screen)

        self.aliens.draw(screen)





if __name__ == '__main__':
    pygame.init()
    screen_weidth= 600
    screen_height= 600
    screen=pygame.display.set_mode((screen_height,screen_weidth))
    clock = pygame.time.Clock()
    game=game()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
