import pygame
import sys
import random

global width, height
width = 480
height = 480

# GRID
gridsize = 20
GridWidth = height / gridsize
GridHeight = width / gridsize

# DIRECTIONS
up = (0 , -1)
down = (0 , 1)
left = (-1 , 0)
right = (1 , 0)

class SnakeObject:
    def __init__(self, ):
        self.length = 1
        self.position = [((width / 2), (height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (255, 255 ,255)

    def GetHeadPosition(self):
        return self.position[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1 ) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.GetHeadPosition()
        x, y = self.direction
        new = (((cur[0] + (x*gridsize)) % width), (cur[1] + (y*gridsize)) % height)
        if len(self.position) > 2 and new in self.position[2:]:
            self.reset()
        else: 
            self.position.insert(0, new)
            if len(self.position) > self.length:
                self.position.pop()

    def reset(self):
        self.length = 1
        self.position = [(((width / 2), (height / 2)))]
        self.direction = random.choice([up, down, left, right])

    def draw(self, surface):
        for p in self.position:
            r = pygame.Rect((p[0] , p[1]), (gridsize , gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface , (255, 255, 255), r , 1)

    def HandleKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class food(object):
    def __init__ (self):
        self.position = (0 , 0)
        self.color = (223 , 163, 49)
        self.RandomizePosition()

    def RandomizePosition(self):
        self.position = (random.randint(0, GridWidth - 1) * gridsize , random.randint(0, GridHeight - 1) * gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize , gridsize))
        pygame.draw.rect(surface , self.color , r)
        pygame.draw.rect(surface , (93, 226, 228), r, 1)


def DrawGrid(surface):
    for y in range(0, int(GridHeight)):
        for x in range(0 , int(GridWidth)):
            if (x + y) % 2 == 0:
                rectangle = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (32, 32, 32), rectangle)
            else:
                DarkRect = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (32, 32, 32), DarkRect)



pygame.init()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

surface = pygame.Surface(screen.get_size())
surface = surface.convert()
DrawGrid(surface)

SnakeObject = SnakeObject()
food = food()

score = 0

while running:
    clock.tick(7)
    SnakeObject.HandleKeys()
    DrawGrid(surface)
    SnakeObject.move()
    if SnakeObject.GetHeadPosition() == food.position:
        SnakeObject.length += 1
        score += 1
        food.RandomizePosition()
    SnakeObject.draw(surface)
    food.draw(surface)
    screen.blit(surface, (0,0))
    pygame.display.update()
