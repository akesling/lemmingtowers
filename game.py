import pygame, math, sys
from pygame.locals import *

SCREEN_SIZE = (1024, 768)
screen = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = (255, 248, 168)
clock = pygame.time.Clock()
FRAMERATE = 30



class Lemming(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 0
    TURN_SPEED = 5
    ACCELERATION = 2

    def __init__(self, position, image="lemming.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = 2
        self.direction = 0
        self.k_left = self.k_right = self.k_up = self.k_down = 0

    def update(self, deltaT):
        if self.position[0] == SCREEN_SIZE[0] or self.position[1] == SCREEN_SIZE[1]:
            self.speed = 0

        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED

#        self.direction = (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed * math.sin(rad)
        y += self.speed * math.cos(rad)
        self.position = (x, y)

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


rect = screen.get_rect()
lemming = Lemming((100,100))
lgroup = pygame.sprite.RenderPlain(lemming)
while 1:
    deltaT = clock.tick(30)
    screen.fill((0, 0, 0))
    lgroup.update(deltaT)
    lgroup.draw(screen)
    pygame.display.flip()
