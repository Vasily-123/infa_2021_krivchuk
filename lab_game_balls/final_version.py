import pygame
from pygame.draw import *
from random import randint
from operator import itemgetter
pygame.init()

FPS = 100
screen = pygame.display.set_mode((800, 800))

number_of_balls = 10
number_of_specials = 100
x = [0] * (number_of_balls)
y = [0] * (number_of_balls)
r = [0] * (number_of_balls)
Vx = [0] * (number_of_balls)
Vy = [0] * (number_of_balls)
color = [0] * (number_of_balls)

x_spec = [0] * (number_of_specials)
y_spec = [0] * (number_of_specials)
Vx_spec = [0] * (number_of_specials)
Vy_spec = [0] * (number_of_specials)

frames_count = []
for i in range (0, number_of_balls):
   frames_count.append((20*i) % 200)
side = 10
end = number_of_balls

def new_ball(number):
    '''рисует новый шарик '''
    global x, y, r, color, Vx, Vy
    x[number] = randint(100, 700)
    y[number] = randint(100, 700)
    r[number] = randint(40, 50)
    Vx[number] = randint(-5, 5)
    Vy[number] = randint(-5, 5)
    color[number] = (randint(0, 255), randint(0, 255), randint(0, 255))
    circle(screen, color[number], (x[number], y[number]), r[number])


def special_target(number):
    '''рисует специальную мишень - квадрат, пермещающийся в случайных направлениях '''
    x_spec[number] = randint(100, 700)
    y_spec[number] = randint(100, 700)
    Vx_spec[number] = randint(-25, 25)
    Vy_spec[number] = randint(-25, 25)
    rect(screen, 'white', pygame.Rect(x_spec[number], y_spec[number], side, side))

def sort_results(text, score):
    '''вносит результаты игрока в таблицу результатов и отсортировывает её
    :param text: имя игрока
    :param score: счёт игрока
    '''
    table = open ('table.txt', 'w')
    with open ('scores.txt', 'a') as output:
      print(text, '"', score, file = output)
    with open ('scores.txt', 'r') as f:
      for string in range (0, 1000, 1):
        stroka = f.readline()
        if stroka != '':
            pairs = stroka.split('" ')
            points.append(pairs)
            a = points[string][1]
            a.rstrip('\n')
            a = int (a)
            points[string][1] = a
    new_list = sorted(points, key=itemgetter(1))
    new_list.reverse()
    print('ТАБЛИЦА ЛИДЕРОВ', file = table)
    for i in range (0, len(new_list), 1):
      new_list[i][1] = str (new_list[i][1])
      print(''.join(new_list[i]), file = table)
    table.close()
                
clock = pygame.time.Clock()

f1 = pygame.font.Font(None, 36)
text1 = f1.render('Очки:', True, 'white')
font = pygame.font.Font (None, 32)
text3 = f1.render('Введите своё имя:', True, 'white')
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color1 = color_inactive

input_box = pygame.Rect(100, 100, 140, 32)

pygame.display.update()


score = '0'
count = 0
points = []
text = ''
for i in range (0, number_of_balls):
    new_ball(i)
for i in range (0, number_of_specials):
    special_target(i)


active = False
done = False
finished = False

while (not finished) and (done == False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color1 = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    done = True
                    screen.fill((0, 0, 0))
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((0, 0, 0))
    txt_surface = font.render(text, True, color1)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color1, input_box, 2)
    screen.blit (text3, (50, 70))
    
    pygame.display.flip()
    clock.tick(30)

while (not finished) and (done == True):
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sort_results(text, score)  
                finished = True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for number in range (0, number_of_balls): 
                    if (event.pos[0]-x[number])**2+(event.pos[1]-y[number])**2<=r[number]**2:
                      count = count + 1
                      score = str (count)
                      circle(screen, 'black', (x[number], y[number]), r[number])
                      new_ball(number)
                      frames_count[number] = 0
                for number in range (0, number_of_specials):
                    if (abs(event.pos[0]-x_spec[number])<=side*2) and (abs(event.pos[1]-y_spec[number])<=side*2):
                      count = count + 10
                      score = str (count)
                      rect(screen, 'black', pygame.Rect(x_spec[number], y_spec[number], side, side))
                      special_target(number)

        text2 = f1.render(score, True, 'white')
        rect(screen, 'black', pygame.Rect(0, 0, 120, 60))
        screen.blit (text1, (10, 10))
        screen.blit (text2, (84, 10))
        
        for number in range (0, number_of_balls):
            if frames_count[number] >= 300:
              frames_count[number] = 0
              circle(screen, 'black', (x[number], y[number]), r[number])
              new_ball(number)                             
            
            circle (screen, 'black', (x[number], y[number]), r[number])
            x[number] += Vx[number]
            y[number] += Vy[number]
            if (x[number]<=r[number]) or (x[number]+r[number]>=800): Vx[number] = -Vx[number]
            if (y[number]<=r[number]) or (y[number]+r[number]>=800): Vy[number] = -Vy[number]
            circle (screen, color[number], (x[number], y[number]), r[number])
            frames_count[number] += 1

        for number in range (0, number_of_specials):
            rect(screen, 'black', pygame.Rect(x_spec[number], y_spec[number], side, side))
            x_spec[number] += Vx_spec[number]
            y_spec[number] += Vy_spec[number]
            Vx_spec[number] = randint(-25, 25)
            Vy_spec[number] = randint(-25, 25)
            if (x_spec[number]<=0): Vx_spec[number] = 50
            if (y_spec[number]<=0): Vy_spec[number] = 50
            if (x_spec[number]>=800): Vx_spec[number] = -50
            if (y_spec[number]>=800): Vy_spec[number] = -50
            rect(screen, 'white', pygame.Rect(x_spec[number], y_spec[number], side, side))
            
        pygame.display.update()

pygame.quit()
