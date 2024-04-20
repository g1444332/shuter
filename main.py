from pygame import *
from random import randint
import math

WIDTH, HEIGHT = 700, 500

x1, y1 = 200, 300
x2, y2 = 400, 300
p_speed, m_speed = 5, 10
FPS = 60

scope_lose, scope_kill = 0, 0

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('da')
background = transform.scale(image.load('images/galaxy.png'), (WIDTH, HEIGHT))

clock = time.Clock()

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer_music.play()
fire_sound = mixer.Sound('sounds/fire.ogg')


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.angle = 90

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
        if keys[K_s] and self.rect.y < HEIGHT - 80:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_SPACE]:
            bullets.add(Bullet("images/bullet.png", self.rect.x + 35, self.rect.y, 10, 5, 15))
        if keys[K_e]:
            bullet1 = Bullet("images/bullet.png", self.rect.x + 17, self.rect.y, 10, 5, 15)
            bullet2 = Bullet("images/bullet.png", self.rect.x + 35, self.rect.y, 10, 5, 15)
            bullet3 = Bullet("images/bullet.png", self.rect.x + 45, self.rect.y, 10, 5, 15)

            bullet1.image = transform.rotate(bullet1.image, 30)
            bullet3.image = transform.rotate(bullet3.image, -30)

            bullet1.angle = 100
            bullet3.angle = 80

            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)

    def set_image(self, player_image):
        self.image = transform.scale(image.load(player_image), self.image.get_size())


class Bullet(GameSprite):
    def update(self):
        radians = math.radians(self.angle)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)

        self.rect.x += dx
        self.rect.y -= dy

        if self.rect.y >= -50:
            pass


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 500:
            self.rect.y = randint(-400, -80)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 500:
            global scope_lose
            scope_lose += 1
            self.rect.y = randint(-400, -80)


bullets = sprite.Group()
# asteroids = sprite.Group()

asteroids = []
for i in range(3):
    asteroids.append(Asteroid('images/asteroid.png', randint(50, 650), randint(-400, -80), randint(1, 2), 50, 50))

enemys = sprite.Group()
for i in range(6):
    enemys.add(Enemy('images/ufo.png', randint(50, 650), randint(-400, -80), randint(1, 2), 50, 50))

rocket = Player('images/rocket.png', 5, HEIGHT - 100, p_speed, 80, 80)

font.init()

font1 = font.Font(None, 70)
font2 = font.Font(None, 30)

win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

        for i in asteroids:
            i.update()
            i.reset()

        for i in enemys:
            i.update()
            i.reset()

        for i in bullets:
            i.update()
            i.reset()

        rocket.update()
        rocket.reset()

        text_scope_lose = font2.render(f'scope lose: {scope_lose}', True, (255, 215, 0))
        text_scope_kill = font2.render(f'scope kill: {scope_kill}', True, (180, 0, 0))

        window.blit(text_scope_lose, (0, 0))
        window.blit(text_scope_kill, (0, 20))

    collides = sprite.groupcollide(enemys, bullets, True, True)
    for c in collides:
        scope_kill += 1
        monster = Enemy('images/ufo.png', randint(50, 650), randint(-400, -80), randint(2, 3), 50, 50)
        enemys.add(monster)

    if sprite.spritecollide(rocket, enemys, False):
        rocket.set_image("images/boom.png")
        rocket.reset()

        finish = True
        window.blit(lose, (200, 200))

    if scope_lose >= 3:
        rocket.set_image("images/boom.png")
        rocket.reset()

        finish = True
        window.blit(lose, (200, 200))

    if scope_kill >= 10:
        finish = True
        window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)
