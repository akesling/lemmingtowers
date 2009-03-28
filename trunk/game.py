import pygame, math, sys
from pygame.locals import *

screen = pygame.display.set_mode((1024, 768))
BACKGROUND = (255, 248, 168)
lemming = pygame.image.load("car.png")
clock = pygame.time.Clock()
FRAMERATE = 30
speed = direction = 0
position = (100, 100)



class lemming(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    TURN_SPEED = 5
    ACCELERATION = 2

    def __init__(self, position, image="lemming.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_up = self.k_down = 0

    def update(self, deltaT):
        self.speed += (k_up + k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED

        self.direction = (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed * math.sin(rad)
        y += self.speed * math.cos(rad)
        self.position = (x, y)

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
