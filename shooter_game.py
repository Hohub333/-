#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

font.init()
font = font.Font(None, 36)

win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('LOSE', True, (255, 0, 0))

lost = 0
score = 0

win_widht1 = 700
win_widht2 = 500

num_fire = 0
rel_time = False

hp = 5

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht1 - 80:  
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top, 15, 30, 30)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y - self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_widht2:
            self.rect.x = randint(80, win_widht1 - 80)
            self.rect.y = 0
            lost = lost + 1

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_widht1 - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80, win_widht1 - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

rocket = Player('rocket.png', 5, win_widht2 -100, 80, 100, 10)


game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYUP:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire.play()
                    rocket.fire()
            
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
        
    if finish != True:
        window.blit(background,(0, 0))
        monster.reset()
        monsters.update()
        monsters.draw(window)
        asteroid.reset()
        asteroids.update()
        asteroids.draw(window)
        rocket.reset()
        rocket.update()
        bullets.update()
        bullets.draw(window)

    if rel_time == True:
        now_time = timer()

        if now_time - last_time < 3:
            reload = font.render()
        
        text = font.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text = font.render('Жизни:' + str(hp), 1, (255, 255, 255))
        window.blit(text, (10, 80))

        collides_2 = sprite.spritecollide(rocket, monsters, False)
        for c in collides_2:
            window.blit(lose, (300, 250))
            finish = True
        
        if score >=100:
            window.blit(win, (300, 250))
            finish = True

        if lost >=3:
            window.blit(lose, (300, 250))
            finish = True

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_widht1 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides_3 = sprite.spritecollide(rocket, asteroids, False)
        for c in collides_3:
            window.blit(lose, (300, 250))
            finish = True
        


    clock.tick(60)
    display.update()