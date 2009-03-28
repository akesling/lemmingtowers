import math
import pygame
from pygame.locals import *
import random
import sys
import time

# Game settings
SCREEN_SIZE = (1024, 768)
screen = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = (0, 0, 0)
clock = pygame.time.Clock()
FRAMERATE = 30
NUM_LEMS = 10
lemsAlive = 0



class Lemming(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    TURN_SPEED = 5
    ACCELERATION = 2

    def __init__(self, position, image="images/lemming.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = 2
        self.direction = 0
        self.k_left = self.k_right = self.k_up = self.k_down = 0

    def update(self, deltaT):
        if self.position[0] == SCREEN_SIZE[0] or self.position[1] == SCREEN_SIZE[1] or self.position[0] == 0 or self.position[1] == 0:
            self.speed = 0

        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < 0:
            self.speed = 0

#        self.direction = (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed * math.sin(rad)
        y += self.speed * math.cos(rad)
        self.position = (x, y)

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



class Tower(pygame.sprite.Sprite):
    def __init__(self, position, image="images/tower.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.image = self.src_image
        self.rect = self.image.get_rect()

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, image="images/default-tile_8.gif"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.image = self.src_image
        self.rect = self.image.get_rect()

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position

# Define the random direction chooser
random.seed(time.time())

# Define the towers/lemming that will be on the map
rect = screen.get_rect()
lgroup = pygame.sprite.RenderPlain(Lemming((100, 100)))  # Add it to the lemming group
tgroup = pygame.sprite.RenderPlain(Tower((100, 200)))
tilegroup = pygame.sprite.RenderPlain(Tile((500, 200)))

framecount = 0
# Start the game loop
while 1:
    framecount = (framecount + 1) % FRAMERATE
    if framecount == 0:
        lemming = Lemming((100, 100))  # Define a lemming
        lgroup.add(lemming)  # Add it to the lemming group
        

    deltaT = clock.tick(30)  # Controll the framerate (which controls game speed)
    screen.fill(BACKGROUND)  # Background color
    lgroup.update(deltaT)  # Update the positions of our objects
    tgroup.update(deltaT)
    tilegroup.update(deltaT)

    # See if our lemming collided with anything
    for l in lgroup:
        if pygame.sprite.spritecollide(l, tgroup, False):  # Collision with a tower
            l.direction += random.choice((90, -90))  # Rotate either left or right

    # Redraw our object positions
    lgroup.draw(screen)
    tgroup.draw(screen)
    tilegroup.draw(screen)

    # Redraw the map with the above changes
    pygame.display.flip()
