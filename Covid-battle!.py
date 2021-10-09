import pygame
import random
import math
from pygame import mixer

pygame.init()


screen= pygame.display.set_mode((800,750))
pygame.display.set_caption("Covid-Battle!")
icon= pygame.image.load('crown.png')
pygame.display.set_icon(icon)

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Background
background_1= pygame.image.load('background.png')

background_go= pygame.image.load('co.png')

# Player
player_img= pygame.image.load('player_knight.png')
player_x= 400
player_y=600
delta_player_x= 0

# Med
med_img= pygame.image.load('medicine.png')
med_x= random.randint(0,690)
med_y= -300
med_y_chnge= 0.8

# Power
pow_img= pygame.image.load('power.png')
pow_x= random.randint(0,690)
pow_y= -500
pow_y_chnge= 0.4


# Gangster:
gang_img= pygame.image.load('corona_evolved_2.png')
gang_x= 380
gang_y= -100
gang_y_chnge= 0.4
count_hit=0

# Enemies, multiple enemies so list
enemy_img= []
enemy_x= []
enemy_y= []
enemy_x_change= []
enemy_y_change= []

num_enemies= 5

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('corona.png'))
    enemy_x.append(random.randint(0,750))
    enemy_y.append(random.randint(0,150))
    enemy_x_change.append(1)
    enemy_y_change.append(0.2)


#Bullet_Vaccine
bul_img= pygame.image.load('vaccine_bullet.png')
bul_x= 0
bul_y= 600
bul_x_change= 0
bul_y_change= 24
bul_state= "Ready"

# Score
score_value=0
font= pygame.font.Font('freesansbold.ttf', 30)
text_x= 10
text_y= 10

# Game over
game_over= pygame.font.Font('freesansbold.ttf', 100)


# Functions:
def enemy(x,y,i):
    enemy_change=screen.blit(enemy_img[i], (x,y))

def player(x,y):
    screen.blit(player_img, (x, y))
    
def bullet_fire(x,y):
    global bul_state, bul_img
    bul_state= 'Fire'
    screen.blit(bul_img, (x+40,y+10))


def is_collision(x1,x2,y1,y2,m):
    dist= math.sqrt(math.pow((x1-x2+8),2)+ math.pow((y1-y2+10),2))
    if dist<= m:
        return True
    else:
        return False
def Victory():
    text= game_over.render("Victory!", True, (255,255,255))
    screen.blit(text, (150,350))

def show_score(x,y):
    score= font.render("Score :"+ str(score_value), True, (255,0,0))
    screen.blit(score, (x,y))

def game_over_text():
    text= game_over.render("GAME OVER", True, (255,255,255))
    screen.blit(text, (150,350))

def med_drop(x,y):
    screen.blit(med_img, (x,y))

def pow_drop(x,y):
    screen.blit(pow_img, (x,y))

def gang_come(x,y):
    screen.blit(gang_img, (x,y))

# game loop
runn= True

while runn:
    # Screen color, Red Green Blue
    screen.fill((0,0,0))
    screen.blit(background_1, (0,0))
    # Quit button
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            runn= False

    # Key check
    if event.type== pygame.KEYDOWN:
        if event.key== pygame.K_LEFT:
            delta_player_x= -4
        if event.key== pygame.K_RIGHT:
            delta_player_x= 4

        if event.key== pygame.K_UP:
            if bul_state== "Ready":
                bullet_sound= mixer.Sound('laser.wav')
                bullet_sound.play()
                bul_x=player_x
                bullet_fire(bul_x, player_y)
            

    if event.type== pygame.KEYUP:
        if event.key== pygame.K_LEFT or event.key== pygame.K_RIGHT:
            delta_player_x= 0


   # player
    player_x+= delta_player_x
    if player_x<=0:
        player_x=0
    elif player_x>685:
        player_x=685

    #bullet movement
    if bul_y<=0:
        bul_y= 600
        bul_state= "Ready"

    if bul_state== "Fire":
        bullet_fire(bul_x, bul_y )
        bul_y-= bul_y_change
    
    # enemies
    for i in range(num_enemies):
        # Game over:
        if enemy_y[i]> 550:
            screen.blit(background_go, (0,0))
            game_over_text()
            enemy_y[i]=2500
            bul_y_change=0
            player_y=2000
            med_y= -2000
            pow_y= -2000
            med_y_chnge=0
            break


        can=score_value/60
        enemy_x[i]+= enemy_x_change[i]
        enemy_y[i]+= enemy_y_change[i] + can/3
        
        if enemy_x[i]<=0:
            enemy_x_change[i]=(0.4 + can)
        elif enemy_x[i]>685:
            enemy_x_change[i]= -(0.4 + can)
        #collision
        collision= is_collision(enemy_x[i], bul_x, enemy_y[i], bul_y,40)
        if  collision== True:
            mixer.Sound('explosion.wav').play()
            # reset bullet
            bul_state= 'Ready'
            bul_y= 600
            score_value+= 10
            enemy_x[i]= random.randint(0,750)
            enemy_y[i]= random.randint(0,150)
        enemy(enemy_x[i], enemy_y[i],i)
    
    # medicine
    med_drop(med_x,med_y)
    med_y+= med_y_chnge
    if med_y> 800:
        med_y=-30
    med_get= is_collision(med_x + 10,player_x, med_y+65 ,player_y,70)
    if med_get== True:
        mixer.Sound('med_collect.wav').play()
        score_value+= 50
        med_y= -300
        med_x= random.randint(0,685)
        bul_y_change*= 1.5 

    # Power
    pow_drop(pow_x,pow_y)
    pow_y+= pow_y_chnge
    if pow_y> 800:
        pow_y=-30
    pow_get= is_collision(bul_x,pow_x, bul_y ,pow_y,30)
    if pow_get== True:
        mixer.Sound('power.wav').play()
        pow_y= -500
        pow_x= random.randint(0,685)
        delta_player_x*= 1.2 

    #Entry of gangster

    if score_value>=120:
        for i in range(num_enemies):
            enemy_y_change[i]= 0
            can=0
            enemy_y[i]= -1000
        pow_y_chnge=0
        pow_y,med_y= -200,-200
        med_y_chnge=0
        mixer.music.stop()
        gang_come(gang_x,gang_y)
        gang_y+= gang_y_chnge
        if gang_y> 800:
            gang_y=-30
        gang_get= is_collision(gang_x + 150,bul_x, gang_y+150 ,bul_y,150)
        if gang_get== True:
            mixer.Sound('explosion.wav').play()
            bul_state= 'Ready'
            bul_y= 600
            score_value+= 10
            count_hit+=1
            print(count_hit)
        if count_hit>=5:
            gang_y=-3000
            screen.fill((0,0,0))
            Victory()
        if gang_y >= 550:
            screen.blit(background_go, (0,0))
            game_over_text()
            enemy_y[i]=2500
            bul_y_change=0
            player_y=2000
            med_y= -2000
            pow_y= -2000
            med_y_chnge=0
            gang_y= 2000


        

    

       # Victory()
    player(player_x, player_y)
    show_score(text_x,text_y)
    pygame.display.update()

