from pygame import *
BLUE = (180, 180, 180)
BLACK = (0, 0, 0)
window = display.set_mode((700, 500))
win = transform.scale(image.load("Win.jpeg"), (700, 500))
lose = transform.scale(image.load("loseee.jpg"), (700, 500))
display.set_caption('Моя первая игра')
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
wall = GameSprite("StoneWall.jpg", 100, 200, 300, 150)
wall_1 = GameSprite("StoneWall.jpg", 200, 100, 150, 250)
wall_2 = GameSprite("StoneWall.jpg", 100, 200, 300, 300)
barriers = sprite.Group()
barriers.add(wall)
barriers.add(wall_1)
barriers.add(wall_2)
bullets = sprite.Group()
class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speedBullet):
        super().__init__(picture, w, h, x, y)
        self.speedBullet = speedBullet
    def update(self):
        self.rect.x += self.speedBullet
        if self.rect.x > 700:
            self.kill()

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.rect.right > 725 or self.rect.left < -15:
            self.rect.x -= self.x_speed
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        if self.rect.bottom > 500 or self.rect.top < -10:
            self.rect.y -= self.y_speed
    def fire(self):
        bullet = Bullet("pickaxe.jpg", 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= 575:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
hero = Player("SteveMinecraft.png", 100, 100, 25, 375, 0, 0)
final = GameSprite("SpawnerZombie.png", 100, 100, 575, 375)
monster = Enemy("Zombie.png", 100, 100, 575, 150, 5)
monsters = sprite.Group()
monsters.add(monster)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                hero.y_speed = -5
            elif e.key == K_a:
                hero.x_speed = -5
            elif e.key == K_s:
                    hero.y_speed = 5
            elif e.key == K_d:
                    hero.x_speed = 5
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                hero.y_speed = 0
            elif e.key == K_a:
                    hero.x_speed = 0
            elif e.key == K_s:
                    hero.y_speed = 0
            elif e.key == K_d:
                    hero.x_speed = 0
    if finish != True:
        window.fill(BLUE)
        hero.update()
        hero.reset()
        wall_1.reset()
        wall_2.reset()
        wall.reset()
        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)
        final.reset()
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True) #!
        if sprite.collide_rect(hero, final):
            finish = True
            window.blit(win,(0,0))
        elif sprite.collide_rect(hero, monster):
            finish = True
            window.blit(lose,(0,0))
    time.delay(50)
    display.update()
    #sprite.spritecolide(player, monsters)