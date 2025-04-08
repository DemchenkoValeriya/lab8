import pygame
import sys
import random

pygame.init()

HEIGHT = 600
WIDTH = 600
grid_SIZE = 20 
grid_WIDTH = WIDTH // grid_SIZE
grid_HEIGHT = HEIGHT // grid_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface(screen.get_size())
surface = surface.convert()

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 255, 0)
        
    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * grid_SIZE)) % WIDTH), (cur[1] + (y * grid_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_SIZE, grid_SIZE))
            pygame.draw.rect(surface, self.color, r)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:  
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)  # Красный цвет еды
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_WIDTH - 1) * grid_SIZE,
                         random.randint(0, grid_HEIGHT - 1) * grid_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (grid_SIZE, grid_SIZE))
        pygame.draw.rect(surface, self.color, r)

snake = Snake()
food = Food()
FPS = 5
score = 0

myfont = pygame.font.SysFont("monospace", 16)

while True:
    snake.handle_keys()
    
    surface.fill((0, 0, 0))  # Чистый черный фон без сетки
    
    snake.move()

    if snake.get_head_position() == food.position:
        snake.length += 1
        score += 1
        FPS += 1
        food.randomize_position()

    snake.draw(surface)
    food.draw(surface)
    
    screen.blit(surface, (0, 0))
    text = myfont.render("Score: {0}".format(score), 1, (255, 255, 255))  # Белый текст счета
    screen.blit(text, (5, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
