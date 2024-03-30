from pygame import *
from random import randint

WIDTH, HEIGHT = 700, 500

x1, y1 = 200, 300
x2, y2 = 400, 300
p_speed, m_speed = 10, 10
FPS = 60

scope_lose = 0
scope_kill = 0

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('da')
background = transform.scale(image.load('images/galaxy.jpg'), (WIDTH, HEIGHT))

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


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 700:
            global scope_lose
            scope_lose += 1
            self.rect.y = randint(-400, -80)



enemys = []
for i in range(6):
    enemys.append(Enemy('images/ufo.png', randint(50, 650), randint(-400, -80), randint(2, 3), 60, 60))

rocket = Player('images/rocket.png', 5, HEIGHT - 100, p_speed, 80, 80)
# ufo = Enemy('ufo.png', randint(100, 600), HEIGHT - 100, 2)

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))



game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))
    for i in enemys:
        i.update()
        i.reset()
    rocket.update()
    rocket.reset()
    text_scope_lose = font.render(f'scope lose: {scope_lose}', True, (255, 215, 0))
    text_scope_kill = font.render(f'scope kill: {scope_kill}', True, (180, 0, 0))

    window.blit(text_scope_lose, (0, 0))
    window.blit(text_scope_kill, (0, 70))

    # if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8) or sprite.collide_rect(player, w9) or sprite.collide_rect(player, w10) or sprite.collide_rect(player, w11):
    #     finish = True
    #     window.blit(lose, (200, 200))
    #     kick.play()

    display.update()
    clock.tick(FPS)
