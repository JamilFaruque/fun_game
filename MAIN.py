from turtle import width
import pygame
import os 
import random

pygame.init()
WIDTH,HEIGHT = 800,700
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space shooting')

# IMPORTING ALL IMAGES
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets','bg.png')),(WIDTH,HEIGHT))
# PLAYER
PLAYER = pygame.image.load(os.path.join('assets','spaceship.png'))
PLAYER_BULLET = pygame.image.load(os.path.join('assets','bullet.png'))
#ENEMY
FURQAN = pygame.image.load(os.path.join('assets','furqan-modified.png'))
ABDUS = pygame.image.load(os.path.join('assets','abdus-modified.png'))
HSIB = pygame.image.load(os.path.join('assets','hsib-modified.png'))
TYF = pygame.image.load(os.path.join('assets','tyf-modified.png'))

ENEMY_BULLET = pygame.image.load(os.path.join('assets','ghost_bullet.png'))

class Bullet:
    def __init__(self,x,y,img):
        self.x = x + 17
        self.y = y 
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self):
        window.blit(self.img,(self.x,self.y))
    def move(self,velocity):
        self.y += velocity

    def collision(self,obj):
        return collide(self,obj)


class Ship:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.bullets = []
        self.COOL_DOWN = 15
        self.cool_down_counter = 0
    
    def draw(self):
        window.blit(self.ship_img,(self.x,self.y))
        for bullet in self.bullets:
            bullet.draw()
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
    
    def shoot(self,bullet_img):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

        if self.cool_down_counter == 0:
            bullet = Bullet(self.x,self.y,bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter += 1
    def move_bullet(self,velocity,obj):
        for bullet in self.bullets:
            bullet.move(velocity)
            if bullet.y > HEIGHT:
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                self.bullets.remove(bullet)
            

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = PLAYER
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move_bullet(self, velocity, objs):
        for bullet in self.bullets:
            bullet.move(velocity)
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        self.bullets.remove(bullet)


        
class Enemy(Ship):
    ENEMY_MAP = {
        'F': FURQAN ,
        'A': ABDUS ,
        'H' : HSIB ,
        'T' : TYF,
    }
    def __init__(self, x, y,pick_enemy):
        super().__init__(x, y)
        self.ship_img = self.ENEMY_MAP[pick_enemy]
        self.mask = pygame.mask.from_surface(self.ship_img)


    def move(self,velocity):
        self.y += velocity


def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))

# MAIN LOOP
def main():
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    timer = 0
    # DISPLAY LABELS
    level = 0
    lives = 5
    lost = False
    main_font = pygame.font.SysFont('comicsans',30)
    lost_font = pygame.font.SysFont('comicsans',60)
    # PLAYER
    player = Player(200,300)
    player_velocity = 5
    # ENEMY
    enemies = []
    enemy_velocity = 2
    live_enemies = 2
    def display():
        clock.tick(FPS)
        window.blit(BG,(0,0))
        # LABELS
        level_label = main_font.render(f'Level : {level}',1,(255,255,255))
        live_label = main_font.render(f'Lives : {lives}',1,(255,255,255))
        window.blit(level_label,(10,10))
        window.blit(live_label,((WIDTH-live_label.get_width()-10),10))

        # ENEMY
        for enemy in enemies:
            enemy.draw()
        # PLAYER
        player.draw()
        if lost:
            lost_label = lost_font.render("YOU LOST!!",1,(255,255,255))
            window.blit(lost_label,((WIDTH-lost_label.get_width())/2,250))
        pygame.display.update()

    while run:
        display()

        if lost:
            timer += 1
            if timer > FPS * 3:
                run = False
            else:
                continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT :
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot(PLAYER_BULLET)

        if len(enemies) == 0:
            level += 1
            if level > 4:
                live_enemies += 4
            live_enemies += 1
            for i in range(live_enemies):
                enemy = Enemy(random.randrange(0,WIDTH-70),random.randrange(-700,0),random.choice(['F','A','H','T']))
                enemies.append(enemy)

        for enemy in enemies:
            enemy.move(enemy_velocity)
            if random.randrange(0,120) == 1 and enemy.y > 0:
                enemy.shoot(ENEMY_BULLET)
            enemy.move_bullet(5,player)
            if enemy.y > HEIGHT or collide(player,enemy):
                lives -= 1
                enemies.remove(enemy)

        if lives <= 0:
            lost = True
            lives = 0
        
    
        player.move_bullet(-5,enemies)

def main_menu():
	run = True
	title_font = pygame.font.SysFont('comicsans', 40)
	while run:
		window.blit(BG,(0,0))
		title_label = title_font.render('Press mouse to begin!',1,(255,255,255))
		window.blit(title_label,((WIDTH-title_label.get_width())/2,320))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
main_menu()