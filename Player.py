# Import the pygame module
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, keysPressed, SCREEN_WIDTH, SCREEN_HEIGHT):
        moveMade = False
        if keysPressed[K_UP]:
            self.rect.move_ip(0, -5)
            moveMade = True
        if keysPressed[K_DOWN]:
            self.rect.move_ip(0, 5)
            moveMade = True
        if keysPressed[K_LEFT]:
            self.rect.move_ip(-5, 0)
            moveMade = True
        if keysPressed[K_RIGHT]:
            self.rect.move_ip(5, 0)
            moveMade = True

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        return moveMade
