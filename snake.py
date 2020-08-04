# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.init()
pygame.display.set_caption('Snake')

red = (255,0,0)
green = (25,133,54)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
yellow = (226,237,7)


class cube(object):
    rows = 25
    w = 500

    def __init__(self, start, color=green):
        self.pos = start
        self.dirnx = 0
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos,color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    message_box('You Lost!', 'Play again...')
                    reset_game(self)
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    message_box('You Lost!', 'Play again...')
                    reset_game(self)
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    message_box('You Lost!', 'Play again...')
                    reset_game(self)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    message_box('You Lost!', 'Play again...')
                    reset_game(self)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset_snake(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    size = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + size
        y = y + size


def redrawWindow(surface):
    global rows, width, s, food, slow, double, legend_text, food_text, slow_text, double_text, score_text, score_value,double_spawned,double_count,slow_count_text,double_count_text,slow_spawned
    surface.fill(color=black)
    s.draw(surface)
    food.draw(surface)
    if slow_spawned:
        slow.draw(surface)
    if double_spawned:
        double.draw(surface)
    drawGrid(width, rows, surface)
    pygame.draw.rect(surface,white,(0,500,width,120))
    surface.blit(legend_text,(10,520))
    surface.blit(food_text, (30, 550))

    surface.blit(slow_text, (30, 570))
    surface.blit(slow_count_text, (140,570))

    surface.blit(double_text, (30, 590))
    surface.blit(double_count_text,(140,590))

    surface.blit(score_text, (180, 520))
    surface.blit(score_value, (180, 550))

    pygame.draw.rect(surface, red, (10, 550, 15, 15))#food marking
    pygame.draw.rect(surface, yellow, (10, 570, 15, 15))#slow marking
    pygame.draw.rect(surface, blue, (10, 590, 15, 15))#double marking


    pygame.display.update()



def randomSnack(rows, item): #will return a cube that can be eaten on the board where the snake isn't
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def reset_game(snake):
    global food, slow, double,slow_timer,double_timer,slow_count,double_count,slow_spawned,double_spawned,num_of_food,num_of_slow,num_of_double
    food = cube(randomSnack(rows, s), color=red)
    snake.reset_snake((10,10))
    slow_timer = 1
    double_timer = 1
    slow_count = 0
    double_count = 0
    slow_spawned = False
    double_spawned = False
    slow = None
    double = None
    num_of_food = 0
    num_of_slow = 0
    num_of_double = 0

def spawn_power_snacks():
    global double_spawned,double_timer,double,slow_spawned,slow_timer,slow,s
    if not double_spawned: #if there is not already this power up
        if double_timer%200==0: #if it is time
            if random.choice([0,1]) == 1:#50% chance of being spawned
                double = cube(randomSnack(rows, s), color=blue)
                double_spawned = True
    if not slow_spawned:
        if slow_timer%200==0:
            if random.choice([0,1]) == 1:
                slow = cube(randomSnack(rows, s), color=yellow)
                slow_spawned = True

def main():
    global width, rows, s, food, slow, double, \
        legend_text, food_text, slow_text, \
        double_text, score_text, score_value,slow_count,\
        double_count,double_spawned,double_timer,slow_count_text,\
        double_count_text,slow_spawned,slow_timer,num_of_food,num_of_slow,\
        num_of_double


    width = 500
    height = 620
    rows = 25
    win = pygame.display.set_mode((width, height))
    s = snake(green, (10, 10))
    food = cube(randomSnack(rows, s), color=red)
    num_of_food=0

    double_spawned = False
    double_timer = 1
    double_count = 0
    double_activated = False
    double = None
    num_of_double = 0



    slow_count = 0
    slow_activated = False
    speed_value = 20
    slow_spawned = False
    slow = None
    slow_timer = 1
    num_of_slow = 0

    titleFont = pygame.font.SysFont("Arial",20)
    textFont = pygame.font.SysFont("Arial", 14)

    legend_text = titleFont.render("Legend",1,black)
    food_text = textFont.render("Food", 1, black)
    slow_text = textFont.render("Slow", 1, black)
    slow_count_text = textFont.render(str(slow_count),1,yellow)
    double_text = textFont.render("Double Food", 1, black)
    double_count_text = textFont.render(str(double_count),1,blue)



    score_text = titleFont.render("Score", 1, black)
    score_value = titleFont.render(str(num_of_food),1,black)

    game_paused = False


    flag = True

    clock = pygame.time.Clock()


    while flag:
        s.move()
        clock.tick(speed_value)
        pygame.time.delay(25)
        if s.body[0].pos == food.pos:
            if double_activated:
                s.addCube()
                s.addCube()
                num_of_food += 2
            else:
                s.addCube()
                num_of_food += 1
            food = cube(randomSnack(rows, s), color=red)

        if slow_spawned:
            if s.body[0].pos == slow.pos: #slows down the game for a number of seconds
                slow_count = 50
                slow_activated = True
                speed_value = 10
                slow_timer = 1
                slow_spawned = False
                double_count=double_count//2
                num_of_slow+=1
        if double_spawned:
            if s.body[0].pos == double.pos: #double length for number of seconds
                double_count = 100
                double_activated = True
                double_timer = 1
                double_spawned = False
                num_of_double+=1

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box('You Lost!', 'Play again...')
                reset_game(s)
                break
        if double_count > 0:
            double_count=double_count-1
        else:
            double_activated = False

        if slow_count > 0:
            slow_count=slow_count-1
        else:
            slow_activated = False
            speed_value = 20


        score_value = titleFont.render(str(num_of_food), 1, black)
        if slow_count == 0:
            slow_count_text = textFont.render(" ", 1, yellow)
        else:
            slow_count_text = textFont.render(str(slow_count), 1, yellow)

        if double_count == 0:
            double_count_text = textFont.render(" ", 1, blue)
        else:
            double_count_text = textFont.render(str(double_count), 1, blue)

        spawn_power_snacks()
        double_timer+=1
        slow_timer+=1
        redrawWindow(win)
main()