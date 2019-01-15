import pygame
import random


# Defining Colors and global Variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
bg = pygame.image.load('background1.png')


#initiating pygame and creating game window
pygame.init()
screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Onslaught")

#loading sound effects and music
pygame.mixer.pre_init(22050,16,2,4096)
pygame.mixer.music.load('music/templeoftime.ogg')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
oof=pygame.mixer.Sound('music/oof.ogg')
pew=pygame.mixer.Sound('music/pew.ogg')
fast1=pygame.mixer.Sound('music/fast1.ogg')
over= pygame.mixer.Sound('music/over.ogg')
star= pygame.mixer.Sound('music/star.ogg')
health=pygame.mixer.Sound('music/health.ogg')
over.set_volume(0.5)
fast1.set_volume(1)
pew.set_volume(0.2)
oof.set_volume(1)
star.set_volume(0.6)
health.set_volume(0.6)

##################Creating Classes########################

#creating the Enemies class
class Enemies(pygame.sprite.Sprite):

    def __init__(self,x,y,color):
        super().__init__()
        self.image=pygame.image.load('icons/creeper.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 1

#creating the Player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icons/steve.png')
        self.rect = self.image.get_rect()
        self.vel=2.5
        self.speed_up_timer = pygame.time.get_ticks()
        self.eight_shot_timer = pygame.time.get_ticks()
        self.invincible_timer = pygame.time.get_ticks()
        self.speed_up_buff = False
        self.eight_shot_buff = False
        self.invincible = False

#creating the bullet class
class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width=4
        self.height=4
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vel = 3.5

#creating the item class
class Items(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        item_images = {}
        item_images['speed_up']=pygame.image.load('icons/speed_up.png')
        item_images['eight_shot']=pygame.image.load('icons/eight_shot.png')
        item_images['star']=pygame.image.load('icons/star.png')
        self.type = random.choice(['speed_up','eight_shot','star'])
        self.image = item_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y

class Consumables(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('icons/heart.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


##########Creating Sprite Groups and Global Variables##################

all_sprites_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()
bullet_up = pygame.sprite.Group()
bullet_down = pygame.sprite.Group()
bullet_right = pygame.sprite.Group()
bullet_left = pygame.sprite.Group()
bullet_ne = pygame.sprite.Group()
bullet_nw = pygame.sprite.Group()
bullet_se = pygame.sprite.Group()
bullet_sw = pygame.sprite.Group()
item_list = pygame.sprite.Group()
player_item_list = pygame.sprite.Group()
consumables_list = pygame.sprite.Group()

global img_size
img_size = 16

player = Player()
#Set position of the player to center of screen
player.rect.x = screen_width/2 - img_size/2
player.rect.y = screen_height/2 - img_size/2
all_sprites_list.add(player)
###################Creating Functions for the Game##################

#function to display score in screen
def draw_score():
    font = pygame.font.Font(None, 30) #font size can be changed later
    text_score = font.render("Score = "+str(score), 0, BLACK)#create the text
    text_lives = font.render("Lives = "+str(lives), 0, BLACK)
    screen.blit(text_score, (3,5)) #where to display
    screen.blit(text_lives, (3,38))


#universal function to draw text on any screen
def draw_text(text,color,x,y):
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x,y)
    screen.blit(text_surface,text_rect)

#Creating the Start Screen
def show_start_screen():
    screen.blit(bg,(0,0))
    draw_text("Welcome to ArcadeOn!", BLACK, screen_width/2, screen_height/3)
    draw_text("Games Available: Onslaught, Rise", BLACK, screen_width/2, screen_height/2)
    draw_text("1 for Onslaught, 2 for Rise!", BLACK, screen_width/2, screen_height/3*2)

    pygame.display.update()
    intro = True
    while intro:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if key[pygame.K_1]:
                onslaught()
            if key[pygame.K_2]:
                rise()

#Creating the GAME OVER screen
def game_over():
    screen.blit(bg,(0,0))
    draw_text("GAME OVER", BLACK, screen_width/2, screen_height/4)
    draw_text("Play Again (SPACE)??? Return to Home (B)", BLACK, screen_width/2, screen_height/2)
    pygame.display.update()
    play_again = False
    while not play_again:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if key[pygame.K_SPACE]:
                game_reset()
                onslaught()
            if key[pygame.K_b]:
                game_reset()
                show_start_screen()

#creating enemy enemy_generator
def enemy_generator_top():
    enemy = Enemies(random.randrange(0,screen_width-16),0,BLUE)
    enemies_list.add(enemy)
    all_sprites_list.add(enemy)

def enemy_generator_bottom():
    enemy = Enemies(random.randrange(0,screen_width-16),screen_height-16,BLUE)
    enemies_list.add(enemy)
    all_sprites_list.add(enemy)

def enemy_generator_right():
    enemy = Enemies(screen_width-16, random.randrange(0,screen_height-16),BLUE)
    enemies_list.add(enemy)
    all_sprites_list.add(enemy)

def enemy_generator_left():
    enemy = Enemies(0, random.randrange(0,screen_height-16),BLUE)
    enemies_list.add(enemy)
    all_sprites_list.add(enemy)

#creating the game reset function
def game_reset():
    lives=3
    score=0
    enemies_list.empty()
    all_sprites_list.empty()
    all_sprites_list.add(player)
    player.rect.x = screen_width/2 - img_size/2
    player.rect.y = screen_height/2 - img_size/2
    bullet_up.empty()
    bullet_down.empty()
    bullet_right.empty()
    bullet_left.empty()
    bullet_ne.empty()
    bullet_nw.empty()
    bullet_se.empty()
    bullet_sw.empty()
    item_list.empty()
    consumables_list.empty()
    player_item_list.empty()

#creating the main game
def onslaught():
    clock = pygame.time.Clock()
    #Settings of the Game
    enemy_spawn_timer = 2000
    item_spawn_timer = 2000
    last_enemy_spawn = 0
    last_item_spawn = 0
    last_shot = 0
    shot_delay = 350
    bullet_vel=3.5
    global score
    score = 0
    global lives
    lives = 3
    spawn_rate = 0.9
    pow = 0



    #starting the game loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        time= pygame.time.get_ticks()

        #generating Enemies
        if score>=50:
            enemy_spawn_timer=1750

        if score>=100:
            enemy_spawn_timer=1500
            spawn_rate = 0.8

        if score>=150:
            enemy_spawn_timer=1250

        if score>=200:
            enemy_spawn_timer=1000
            spawn_rate = 0.75

        if score>=250:
            enemy_spawn_timer=750
            spawn_rate=0.65


        if time - last_enemy_spawn >= enemy_spawn_timer:
            enemy_generator_top()
            enemy_generator_bottom()
            enemy_generator_right()
            enemy_generator_left()
            last_enemy_spawn=time

        #generating a heart every 100 score
        if score%100 == 0 and score != 0 and len(consumables_list)==0 and lives<5:
            heart = Consumables(random.randrange(screen_width-16),random.randrange(screen_height-16))
            all_sprites_list.add(heart)
            consumables_list.add(heart)

        #Player Move Controls
        key = pygame.key.get_pressed()

        if key[pygame.K_w] and player.rect.y>player.vel:
            player.rect.y -= player.vel

        if key[pygame.K_s] and player.rect.y <screen_height - img_size - player.vel:
            player.rect.y += player.vel

        if key[pygame.K_d] and player.rect.x<screen_width - img_size - player.vel:
            player.rect.x += player.vel

        if key[pygame.K_a] and player.rect.x>player.vel:
            player.rect.x -= player.vel

        #Player Shoot Controls
        now = pygame.time.get_ticks()
        if key[pygame.K_UP]:
            if now - last_shot >= shot_delay:
                if player.eight_shot_buff==True:
                    last_shot = now
                    bulletup = Bullet()
                    bulletdown = Bullet()
                    bulletright = Bullet()
                    bulletleft = Bullet()
                    bulletne = Bullet()
                    bulletnw = Bullet()
                    bulletse = Bullet()
                    bulletsw = Bullet()
                    bulletup.rect.x = player.rect.x + img_size/2 - bulletup.width/2
                    bulletup.rect.y = player.rect.y + img_size/2 - bulletup.height/2
                    bulletdown.rect.x = player.rect.x + img_size/2 - bulletdown.width/2
                    bulletdown.rect.y = player.rect.y + img_size/2 - bulletdown.height/2
                    bulletright.rect.x = player.rect.x + img_size/2 - bulletright.width/2
                    bulletright.rect.y = player.rect.y + img_size/2 - bulletright.height/2
                    bulletleft.rect.x = player.rect.x + img_size/2 - bulletleft.width/2
                    bulletleft.rect.y = player.rect.y + img_size/2 - bulletleft.height/2
                    bulletne.rect.x = player.rect.x + img_size/2 - bulletne.width/2
                    bulletne.rect.y = player.rect.y + img_size/2 - bulletne.height/2
                    bulletnw.rect.x = player.rect.x + img_size/2 - bulletnw.width/2
                    bulletnw.rect.y = player.rect.y + img_size/2 - bulletnw.height/2
                    bulletse.rect.x = player.rect.x + img_size/2 - bulletse.width/2
                    bulletse.rect.y = player.rect.y + img_size/2 - bulletse.height/2
                    bulletsw.rect.x = player.rect.x + img_size/2 - bulletsw.width/2
                    bulletsw.rect.y = player.rect.y + img_size/2 - bulletsw.height/2
                    all_sprites_list.add(bulletup,bulletdown,bulletright,bulletleft,bulletne,bulletnw,bulletse,bulletsw)
                    bullet_up.add(bulletup)
                    bullet_down.add(bulletdown)
                    bullet_right.add(bulletright)
                    bullet_left.add(bulletleft)
                    bullet_ne.add(bulletne)
                    bullet_nw.add(bulletnw)
                    bullet_se.add(bulletse)
                    bullet_sw.add(bulletsw)
                else:
                    last_shot = now
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + img_size/2 - bullet.width/2
                    bullet.rect.y = player.rect.y + img_size/2 - bullet.height/2
                    all_sprites_list.add(bullet)
                    bullet_up.add(bullet)

        if key[pygame.K_DOWN]:
            if now - last_shot >= shot_delay:
                if player.eight_shot_buff==True:
                    last_shot = now
                    bulletup = Bullet()
                    bulletdown = Bullet()
                    bulletright = Bullet()
                    bulletleft = Bullet()
                    bulletne = Bullet()
                    bulletnw = Bullet()
                    bulletse = Bullet()
                    bulletsw = Bullet()
                    bulletup.rect.x = player.rect.x + img_size/2 - bulletup.width/2
                    bulletup.rect.y = player.rect.y + img_size/2 - bulletup.height/2
                    bulletdown.rect.x = player.rect.x + img_size/2 - bulletdown.width/2
                    bulletdown.rect.y = player.rect.y + img_size/2 - bulletdown.height/2
                    bulletright.rect.x = player.rect.x + img_size/2 - bulletright.width/2
                    bulletright.rect.y = player.rect.y + img_size/2 - bulletright.height/2
                    bulletleft.rect.x = player.rect.x + img_size/2 - bulletleft.width/2
                    bulletleft.rect.y = player.rect.y + img_size/2 - bulletleft.height/2
                    bulletne.rect.x = player.rect.x + img_size/2 - bulletne.width/2
                    bulletne.rect.y = player.rect.y + img_size/2 - bulletne.height/2
                    bulletnw.rect.x = player.rect.x + img_size/2 - bulletnw.width/2
                    bulletnw.rect.y = player.rect.y + img_size/2 - bulletnw.height/2
                    bulletse.rect.x = player.rect.x + img_size/2 - bulletse.width/2
                    bulletse.rect.y = player.rect.y + img_size/2 - bulletse.height/2
                    bulletsw.rect.x = player.rect.x + img_size/2 - bulletsw.width/2
                    bulletsw.rect.y = player.rect.y + img_size/2 - bulletsw.height/2
                    all_sprites_list.add(bulletup,bulletdown,bulletright,bulletleft,bulletne,bulletnw,bulletse,bulletsw)
                    bullet_up.add(bulletup)
                    bullet_down.add(bulletdown)
                    bullet_right.add(bulletright)
                    bullet_left.add(bulletleft)
                    bullet_ne.add(bulletne)
                    bullet_nw.add(bulletnw)
                    bullet_se.add(bulletse)
                    bullet_sw.add(bulletsw)
                else:
                    last_shot = now
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + img_size/2 - bullet.width/2
                    bullet.rect.y = player.rect.y + img_size/2 - bullet.height/2
                    all_sprites_list.add(bullet)
                    bullet_down.add(bullet)

        if key[pygame.K_RIGHT]:
            if now - last_shot >= shot_delay:
                if player.eight_shot_buff==True:
                    last_shot = now
                    bulletup = Bullet()
                    bulletdown = Bullet()
                    bulletright = Bullet()
                    bulletleft = Bullet()
                    bulletne = Bullet()
                    bulletnw = Bullet()
                    bulletse = Bullet()
                    bulletsw = Bullet()
                    bulletup.rect.x = player.rect.x + img_size/2 - bulletup.width/2
                    bulletup.rect.y = player.rect.y + img_size/2 - bulletup.height/2
                    bulletdown.rect.x = player.rect.x + img_size/2 - bulletdown.width/2
                    bulletdown.rect.y = player.rect.y + img_size/2 - bulletdown.height/2
                    bulletright.rect.x = player.rect.x + img_size/2 - bulletright.width/2
                    bulletright.rect.y = player.rect.y + img_size/2 - bulletright.height/2
                    bulletleft.rect.x = player.rect.x + img_size/2 - bulletleft.width/2
                    bulletleft.rect.y = player.rect.y + img_size/2 - bulletleft.height/2
                    bulletne.rect.x = player.rect.x + img_size/2 - bulletne.width/2
                    bulletne.rect.y = player.rect.y + img_size/2 - bulletne.height/2
                    bulletnw.rect.x = player.rect.x + img_size/2 - bulletnw.width/2
                    bulletnw.rect.y = player.rect.y + img_size/2 - bulletnw.height/2
                    bulletse.rect.x = player.rect.x + img_size/2 - bulletse.width/2
                    bulletse.rect.y = player.rect.y + img_size/2 - bulletse.height/2
                    bulletsw.rect.x = player.rect.x + img_size/2 - bulletsw.width/2
                    bulletsw.rect.y = player.rect.y + img_size/2 - bulletsw.height/2
                    all_sprites_list.add(bulletup,bulletdown,bulletright,bulletleft,bulletne,bulletnw,bulletse,bulletsw)
                    bullet_up.add(bulletup)
                    bullet_down.add(bulletdown)
                    bullet_right.add(bulletright)
                    bullet_left.add(bulletleft)
                    bullet_ne.add(bulletne)
                    bullet_nw.add(bulletnw)
                    bullet_se.add(bulletse)
                    bullet_sw.add(bulletsw)
                else:
                    last_shot = now
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + img_size/2 - bullet.width/2
                    bullet.rect.y = player.rect.y + img_size/2 - bullet.height/2
                    all_sprites_list.add(bullet)
                    bullet_right.add(bullet)

        if key[pygame.K_LEFT]:
            if now - last_shot >= shot_delay:
                if player.eight_shot_buff==True:
                    last_shot = now
                    bulletup = Bullet()
                    bulletdown = Bullet()
                    bulletright = Bullet()
                    bulletleft = Bullet()
                    bulletne = Bullet()
                    bulletnw = Bullet()
                    bulletse = Bullet()
                    bulletsw = Bullet()
                    bulletup.rect.x = player.rect.x + img_size/2 - bulletup.width/2
                    bulletup.rect.y = player.rect.y + img_size/2 - bulletup.height/2
                    bulletdown.rect.x = player.rect.x + img_size/2 - bulletdown.width/2
                    bulletdown.rect.y = player.rect.y + img_size/2 - bulletdown.height/2
                    bulletright.rect.x = player.rect.x + img_size/2 - bulletright.width/2
                    bulletright.rect.y = player.rect.y + img_size/2 - bulletright.height/2
                    bulletleft.rect.x = player.rect.x + img_size/2 - bulletleft.width/2
                    bulletleft.rect.y = player.rect.y + img_size/2 - bulletleft.height/2
                    bulletne.rect.x = player.rect.x + img_size/2 - bulletne.width/2
                    bulletne.rect.y = player.rect.y + img_size/2 - bulletne.height/2
                    bulletnw.rect.x = player.rect.x + img_size/2 - bulletnw.width/2
                    bulletnw.rect.y = player.rect.y + img_size/2 - bulletnw.height/2
                    bulletse.rect.x = player.rect.x + img_size/2 - bulletse.width/2
                    bulletse.rect.y = player.rect.y + img_size/2 - bulletse.height/2
                    bulletsw.rect.x = player.rect.x + img_size/2 - bulletsw.width/2
                    bulletsw.rect.y = player.rect.y + img_size/2 - bulletsw.height/2
                    all_sprites_list.add(bulletup,bulletdown,bulletright,bulletleft,bulletne,bulletnw,bulletse,bulletsw)
                    bullet_up.add(bulletup)
                    bullet_down.add(bulletdown)
                    bullet_right.add(bulletright)
                    bullet_left.add(bulletleft)
                    bullet_ne.add(bulletne)
                    bullet_nw.add(bulletnw)
                    bullet_se.add(bulletse)
                    bullet_sw.add(bulletsw)
                else:
                    last_shot = now
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + img_size/2 - bullet.width/2
                    bullet.rect.y = player.rect.y + img_size/2 - bullet.height/2
                    all_sprites_list.add(bullet)
                    bullet_left.add(bullet)

        # Bullet Move and Collision Detector
        for bullet in bullet_up:
            bullet.rect.y-=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_up.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.y < -10:
                bullet_right.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_down:
            bullet.rect.y+=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_down.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.y > screen_height + 10:
                bullet_right.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_right:
            bullet.rect.x+=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_right.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x > screen_width +10:
                bullet_right.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_left:
            bullet.rect.x-=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_left.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x <-10:
                bullet_right.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_ne:
            bullet.rect.x+=bullet_vel
            bullet.rect.y-=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_ne.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x > screen_width+10 or bullet.rect.y<-10:
                bullet_ne.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_nw:
            bullet.rect.x-=bullet_vel
            bullet.rect.y-=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_nw.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x < -10 or bullet.rect.y<-10:
                bullet_nw.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_se:
            bullet.rect.x+=bullet_vel
            bullet.rect.y+=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_se.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x > screen_width+10 or bullet.rect.y>screen_height+10:
                bullet_se.remove(bullet)
                all_sprites_list.remove(bullet)

        for bullet in bullet_sw:
            bullet.rect.x-=bullet_vel
            bullet.rect.y+=bullet_vel
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies_list, True)
            for enemy in enemy_hit_list:
                pew.play()
                bullet_sw.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)
            if bullet.rect.x < -10 or bullet.rect.y>screen_height+10:
                bullet_sw.remove(bullet)
                all_sprites_list.remove(bullet)

        #Enemy AI (This somehow works?... I'm a genius)
        for enemy in enemies_list:
            if enemy.rect.x<player.rect.x:
                enemy.rect.x+=enemy.vel
            if enemy.rect.x>player.rect.x:
                enemy.rect.x-=enemy.vel
            if enemy.rect.y<player.rect.y:
                enemy.rect.y+=enemy.vel
            if enemy.rect.y>player.rect.y:
                enemy.rect.y-=enemy.vel


        #player collisions
        if lives>=1:
            player_hit_list = pygame.sprite.spritecollide(player, enemies_list, True)
            if player.invincible==False:
                for Player in player_hit_list:
                    oof.play()
                    lives-=1
                    if lives==0:
                        oof.play()
                        game_over()
            elif player.invincible == True:
                if random.random()>spawn_rate and len(item_list)==0:
                    new_item = Items(enemy.rect.x,enemy.rect.y)
                    all_sprites_list.add(new_item)
                    item_list.add(new_item)



        hits = pygame.sprite.spritecollide(player, item_list, True)
        now=pygame.time.get_ticks()

        #adding the power up effects
        for hit in hits:

            if hit.type == 'speed_up':
                fast1.play()
                player.speed_up_timer=pygame.time.get_ticks()
                player.vel=3.5
                bullet_vel=5
                shot_delay = 150
                player.speed_up_buff = True
                player_item_list.add(hit)
                all_sprites_list.remove(hit)

            if hit.type == 'eight_shot':
                over.play()
                player.eight_shot_timer=pygame.time.get_ticks()
                player.eight_shot_buff = True
                player_item_list.add(hit)
                all_sprites_list.remove(hit)

            if hit.type =='star':
                star.stop()
                star.play()
                player.invincible_timer = pygame.time.get_ticks()
                player.invincible = True
                player_item_list.add(hit)
                all_sprites_list.remove(hit)

        #removing the power up effects after a certain amount of time
        if len(player_item_list)!=0:
            if player.speed_up_buff==True and now-player.speed_up_timer>=5000:
                player.speed_up_timer=now
                player.speed_up_buff=False
                player.vel=2.5
                shot_delay = 350
                player_item_list.remove(hit)
                item_list.remove(hit)

            if player.eight_shot_buff==True and now-player.eight_shot_timer>=5000: #FIXED
                player.eight_shot_timer=now
                player.eight_shot_buff=False
                player_item_list.remove(hit)
                item_list.remove(hit)

            if player.invincible == True and now - player.invincible_timer >=8000:
                player.invincible_timer = now
                player.invincible=False
                player_item_list.remove(hit)
                item_list.remove(hit)
                star.stop()

        consume = pygame.sprite.spritecollide(player,consumables_list, True)
        for heart in consume:
            health.play()
            lives+=1
            consumables_list.remove(heart)
            all_sprites_list.remove(heart)


        #draw stuff on the screen
        screen.fill(WHITE)
        screen.blit(bg, (0,0))
        all_sprites_list.draw(screen)
        draw_score()

        pygame.display.update()
        clock.tick(60)
        #end of game loop function




#starting the game from start screen
show_start_screen()
pygame.quit()
