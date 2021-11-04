import math
from random import randint as rnd, choice
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy += -9.8*0.1
        if self.x > 790 and (self.vx > 0):
            self.vx = -self.vx
        if (self.y > 600) and (self.vy <= 0):
            self.vy = -self.vy*0.5
            self.vx = self.vx*0.8
        if (abs(self.vy) < 1) and (abs(self.y - 600) < 10):
            self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)**(1/2) < (self.r + obj.r):
            return True
        else:
            return False


class Shot:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 4
        self.vx = 0
        self.vy = 0
        self.color = ('blue')

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)**(1/2)<(self.r + obj.r):
            return True
        else:
            return False


class Gun:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.vx = 10
        self.x = x
        self.y = y
        self.color = BLACK
        self.live = 3

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, shot_type):
        if shot_type == 1:
            new_ball = Ball(self.screen, gun[active].x, gun[active].y)
            new_ball.r += 5
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            balls.append(new_ball)
            self.f2_on = 0
            self.f2_power = 10
        if shot_type == 2:
            for i in range(3):
                shot = Shot(self.screen, gun[active].x, gun[active].y)
                self.an = math.atan2((event.pos[1] - shot.y), (event.pos[0] - shot.x))
                shot.vx = self.f2_power * (math.cos((self.an)+(i-1)*math.pi/6))
                shot.vy = - self.f2_power * (math.sin((self.an)+(i-1)*math.pi/6))
                shots.append(shot)
            self.f2_on = 0
            self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] != self.x:
              self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
            else:
              self.an = math.pi/2
            if (event.pos[0] < self.x):
                self.an += math.pi
        if self.f2_on:
            self.color = 'ORANGE'
        else:
            self.color = 'BLACK'

    def draw(self):
        pygame.draw.rect(screen, 'green4', (self.x-20, self.y-10, 40, 20))
        pygame.draw.line(screen, self.color, [self.x, self.y], [self.x + 2*math.cos(self.an)*self.f2_power, self.y + 2*math.sin(self.an)*self.f2_power], 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = "ORANGE"
        else:
            self.color = BLACK

    def move(self):
        self.x += self.vx
        if (self.x > 800) or (self.x < 0):
            self.vx = -self.vx


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 1
        self.x = rnd(200, 400)
        self.y = rnd(200, 400)
        self.r = rnd(2, 50)
        self.vx = rnd(10, 20)
        self.vy = rnd(10, 20)
        self.color = RED
        self.draw()
        self.phi = 0

    def move1(self):
        """Переместить мишень по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x > 790 and (self.vx >= 0):
            self.vx = -self.vx
        if self.x < 0 and (self.vx <= 0):
            self.vx = -self.vx
        if (self.y > 500) and (self.vy <= 0):
            self.vy = -self.vy
        if (self.y < 100) and (self.vy >= 0):
            self.vy = -self.vy

    def move2(self):
        self.x += self.vx
        self.y -= self.vy
        self.vx = rnd(-40, 40)
        self.vy = rnd(-40, 40)
        if self.x > 790:
            self.vx = -50
        if self.x < 0:
            self.vx = 50
        if self.y > 400:
            self.vy = 50
        if self.y < 200:
            self.vy = -50

    def move3(self):
        self.x += 10*math.cos(self.phi)
        self.y -= 10*math.sin(self.phi)
        self.phi = self.phi + 0.1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r) 


class Bomb:
    def __init__(self, screen: pygame.Surface, obj1, obj2):
        self.screen = screen
        self.x = obj1.x
        self.y = obj1.y
        self.r = 10
        if obj1.y > obj2.y:
            self.vy = -10
        else:
            self.vy = 10

    def move(self):
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(self.screen, 'black', (self.x, self.y), self.r)

    def hittest(self, obj):
        if ((self.x-obj.x)**2+(self.y-obj.y)**2)**(1/2)<(self.r + 10):
            return True
        else:
            return False


def make_text():
    text2 = f1.render(count, True, 'black')
    live1 = f1.render(str(gun[1].live), True, 'green3')
    live2 = f1.render(str(gun[0].live), True, 'green3')
    screen.blit(text1, (10, 10))
    screen.blit(text2, (84, 10))
    screen.blit(tank1, (300, 10))
    screen.blit(live1, (390, 10))
    screen.blit(tank2, (500, 10))
    screen.blit(live2, (590, 10))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []
shots = []
gun = [0, 0]
targets = [0, 0, 0]
bombs = []
score = 0
bullet = 0
strike = 0
active = 0
shot_type = 1
f1 = pygame.font.Font(None, 36)
text1 = f1.render('Очки:', True, 'black')
text3 = f1.render('Вы уничтожили цель за', True, 'black')
text5 = f1.render('Все ваши танки умерли!', True, 'black')
your_score = f1.render('Ваш счёт:', True, 'black')
tank1 = f1.render('Танк 1:', True, 'green3')
tank2 = f1.render('Танк 2:', True, 'green3')

gun[1] = Gun(screen, 20, 550)
gun[0] = Gun(screen, 780, 50)
live1 = f1.render(str(gun[1].live), True, 'green3')
live2 = f1.render(str(gun[0].live), True, 'green3')
for t in range(3):
    targets[t] = Target()

clock = pygame.time.Clock()
finished = False
rules = False

while (not finished) and (not rules):
    screen.fill(WHITE)
    introduction = f1.render('В этой игре вам предстоит сбивать цели с помощью танков', True, 'black')
    screen.blit(introduction, (20, 20))
    introduction = f1.render('У каждого танка три жизни, уклоняйтесь от падающих бомб', True, 'black')
    screen.blit(introduction, (20, 50))
    introduction = f1.render('Управление:', True, 'black')
    screen.blit(introduction, (20, 80))
    introduction = f1.render('Стрелки вправо и влево - движение танков', True, 'black')
    screen.blit(introduction, (20, 110))
    introduction = f1.render('Цифры 1 и 2 - переключение между видами снарядов ', True, 'black')
    screen.blit(introduction, (20, 140))
    introduction = f1.render('ПКМ - переключение между танками', True, 'black')
    screen.blit(introduction, (20, 170))
    introduction = f1.render('ЛКМ - огонь', True, 'black')
    screen.blit(introduction, (20, 200))
    introduction = f1.render('Количество очков за раунд: 10 - кол-во выстрелов', True, 'black')
    screen.blit(introduction, (20, 230))
    introduction = f1.render('Для начала игры нажмите ЛКМ', True, 'black')
    screen.blit(introduction, (20, 300))
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rules = True


while not finished:
    screen.fill(WHITE)
    for g in gun:
        if g.live > 0:
            g.draw()
    count = str(score)
    make_text()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            if gun[active].live > 0:
                gun[active].fire2_start(event)
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):
            if gun[1-active].live > 0:
                active = 1 - active
        elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            if gun[active].live > 0:
                gun[active].fire2_end(event, shot_type)
                bullet += 1
        elif event.type == pygame.MOUSEMOTION:
            gun[active].targetting(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gun[active].vx = 10
            elif event.key == pygame.K_LEFT:
                gun[active].vx = -10
            if event.key == pygame.K_1:
                shot_type = 1
            if event.key == pygame.K_2:
                shot_type = 2
    gun[1].move()
    gun[0].move()
    targets[0].move3()
    targets[1].move1()
    targets[2].move2()

    for target in targets:
        if target.live == 1:
            for g in gun:
                if g.live > 0:
                    if abs(target.x - g.x) < 5:
                        bomb = Bomb(screen, target, g)
                        bombs.append(bomb)
            target.draw()
    for bomb in bombs:
        bomb.move()
        bomb.draw()
        for g in gun:
            if bomb.hittest(g) and g.live > 0:
                g.live -= 1
    for s in shots:
        s.move()
        s.draw()
    for b in balls:
        b.move()
        b.draw()
    for target in targets:
        for s in shots:
            if s.hittest(target) and target.live:
                strike += 1
                target.live = 0
        for b in balls:
            if b.hittest(target) and target.live:
                strike += 1
                target.live = 0
    if strike == 3:
        k = str(bullet)+' выстрелов'
        text4 = f1.render(k, True, 'black')
        screen.blit(text3, (200, 200))
        screen.blit(text4, (500, 200))
        make_text()
        pygame.display.update()
        t = 0
        while t < 60:
            clock.tick(FPS)
            screen.fill(WHITE)
            gun[1].draw()
            gun[0].draw()
            for s in shots:
                s.move()
                s.draw()
            for b in balls:
                b.move()
                b.draw()
            screen.blit(text3, (200, 200))
            screen.blit(text4, (495, 200))
            make_text()
            pygame.display.update()
            t += 1
        score += 10 - bullet
        bullet = 0
        strike = 0
        for t in range(3):
            targets[t] = Target()
    if gun[1].live == 0 and gun[0].live == 0:
        screen.blit(text5, (200, 200))
        screen.blit(your_score, (200, 250))
        schot = f1.render(str(score), True, 'red')
        screen.blit(schot, (323, 250))
        pygame.display.update()
    for i in range(2):
        if (gun[i].live == 0) and (i == active):
            active = 1 - active

    pygame.display.update()
    gun[active].power_up()

pygame.quit()
