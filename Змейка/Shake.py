import pygame
from random import randrange
import keyboard

class Control:
    def __init__(self, dirs: dict, x_y: list, key: str) -> None:
        self.dirs = dirs
        self.x_y = x_y
        self.key = key

    def __call__(self, _):
        if self.key == 'W' and self.dirs['W']:
            self.x_y[:] = [0, -1]
            self.dirs.update({'W': True, 'S': False, 'A': True, 'D': True, })
        if self.key == 'S' and self.dirs['S']:
            self.x_y[:] = [0, 1]
            self.dirs.update({'W': False, 'S': True, 'A': True, 'D': True, })
        if self.key == 'A' and self.dirs['A']:
            self.x_y[:] = [-1, 0]
            self.dirs.update({'W': True, 'S': True, 'A': True, 'D': False, })
        if self.key == 'D' and self.dirs['D']:
            self.x_y[:] = [1, 0]
            self.dirs.update({'W': True, 'S': True, 'A': False, 'D': True, })
        print(self.dirs)


def run_ctrl():
    up = Control(dirs, x_y, 'W')
    down = Control(dirs, x_y, 'S')
    left = Control(dirs, x_y, 'A')
    right = Control(dirs, x_y, 'D')
    keyboard.on_press_key('W', up)
    keyboard.on_press_key('S', down)
    keyboard.on_press_key('A', left)
    keyboard.on_press_key('D', right)


RES = 800
SIZE = 80

x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
length = 1
snake = [(x, y)]
x_y = [0, 0]
dx, dy = 0, 0
score = 0
fps = 1

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)

run_ctrl() #управление

while True:
    dx, dy = x_y    #передача значение управление
    sc.fill(pygame.Color('black'))

    # Счёт
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    sc.blit(render_score, (5, 5))
    # Движение змейки
    x += dx * SIZE
    y += dy * SIZE
    snake.append((x, y))
    snake = snake[-length:]
    # отрисовка
    [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
    pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))
    # Скушать яблочко
    if snake[-1] == apple:
        apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        length += 1
        fps += 0.1
        score += 1

    # game over
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            sc.blit(render_end, (RES // 2 - 180, RES // 2.5))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

    pygame.display.flip()
    clock.tick(fps)
# закрытие приложения

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
