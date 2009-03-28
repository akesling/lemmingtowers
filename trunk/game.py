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

    def fire():
        pass

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position


# Define the random direction chooser
random.seed(time.time())

# Define the towers/lemming that will be on the map
rect = screen.get_rect()
lemming = Lemming((100, 100))  # Define a lemming
lgroup = pygame.sprite.RenderPlain(lemming)  # Add it to the lemming group
tower = Tower((100, 200))  # Same for towers
tgroup = pygame.sprite.RenderPlain(tower)

# Start the game loop
while 1:
    deltaT = clock.tick(30)  # Controll the framerate (which controls game speed)
    screen.fill(BACKGROUND)  # Background color
    lgroup.update(deltaT)  # Update the positions of our objects
    tgroup.update(deltaT)

    # See if our lemming collided with anything
    for l in lgroup:
        if pygame.sprite.spritecollide(l, tgroup, False):  # Collision with a tower
            l.direction += random.choice((90, -90))  # Rotate either left or right

    # Redraw our object positions
    lgroup.draw(screen)
    tgroup.draw(screen)

    # Redraw the map with the above changes
    pygame.display.flip()
