from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
               
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed 
            
    def fire(self):
        global bullet 
        bullet = Bullet("bullet2.jpg", self.rect.centerx, self.rect.top, -5) 
        bullets.add(bullet)    
 
lost = 0
score = 0
max_lost = 3
goal = 10
lost2 = 0
num_fire = 0
rel_time = False

     
class Enemy(GameSprite):
    def update(self):
        self.rect.y += randint(2, 4)
        global lost
        global font1
        global text_lose
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = -50
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += randint(1, 3)
        global lost2
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = -50  
  

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y < 0:
            self.kill()                   

win_height = 500
win_leight = 700
speed = 5

font.init()
font1 = font.SysFont('Arial', 60)
font2 = font.SysFont('Arial', 36)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 0, 0))
win = font1.render('you win', True, (255, 215, 0))
lose = font1.render('you lose', True, (180, 0, 0))

mixer.init()
mixer.music.load('may3.ogg')
mixer.music.play()
fire_sound = mixer.Sound('may.ogg')

window = display.set_mode((win_leight, win_height))
display.set_caption('шутер')
background = transform.scale(image.load('images2.jpg'), (win_leight, win_height))

run = True
clock = time.Clock()
FPS = 60
finish = False

rocket = Player("images.jpg", 350, win_height-80, 10)
monster = Enemy('demon.png', randint(80, 620), 0, randint(1,3))
monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy('demon.png', randint(80, 620), 0, randint(1,3)))
bullets = sprite.Group()
asteroinds = sprite.Group()
for i in range(2):
    asteroinds.add(Asteroid('asteroid.png', randint(80, 620), 0, randint(1,3)))

    
while run:                 
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()   
                         
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
            
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                           
    if finish != True:
        window.blit(background,(0,0))
        window.blit(text_lose, (10,50))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroinds.draw(window)
        asteroinds.update()
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('перезарядка', 1, (252, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
    
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('demon.png', randint(80, 620), 0, randint(1,3))
            monsters.add(monster)
            
        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            
        text = font2.render('Счет:' + str(score), 1, (255, 0, 0))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 50))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroinds:
            a.kill()
            
        time.delay(3000)
        
        for i in range(5):
            monsters.add(monster)
            monster = Enemy('demon.png', randint(80, 620), 0, randint(1,3))
        
        for i in range(2):
            asteroid = Asteroid('asteroid.png', randint(80, 620), 0, randint(1,3))
            asteroinds.add(asteroid)
    time.delay(30)
        
        
            
        

            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    display.update()
    clock.tick(FPS)