# Import the pygame module
import pygame

from pygame.locals import (
    K_a,
    K_s,
    K_d,
    K_w
)

class Human(pygame.sprite.Sprite):
    def __init__(self):
        super(Human, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.replaceSurf = pygame.Surface((10, 10))
        self.surf.fill((0, 255, 0))
        self.replaceSurf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(100, 100)

        self.moveUp = True
        self.moveDown = True
        self.moveLeft = True
        self.moveRight = True

    def update(self, keysPressed, SCREEN_WIDTH, SCREEN_HEIGHT, wallGroup, humanScreen):
        moveMade = False
        if keysPressed[K_w] and self.moveUp:
            humanScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(0, -5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_s] and self.moveDown:
            humanScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(0, 5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_a] and self.moveLeft:
            humanScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(-5, 0)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_d] and self.moveRight:
            humanScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(5, 0)
            moveMade = True
            self.checkDirections(wallGroup)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        humanScreen.blit(self.surf, self.rect)

        return moveMade

    def checkDirections(self, wallGroup):
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, wallGroup) != None:
                self.moveUp = False
            else:
                self.moveUp = True
            self.rect.move_ip(0, 10)
            if pygame.sprite.spritecollideany(self, wallGroup) != None:
                self.moveDown = False
            else:
                self.moveDown = True
            self.rect.move_ip(-5, -5)
            if pygame.sprite.spritecollideany(self, wallGroup) != None:
                self.moveLeft = False
            else:
                self.moveLeft = True
            self.rect.move_ip(10, 0)
            if pygame.sprite.spritecollideany(self, wallGroup) != None:
                self.moveRight = False
            else:
                self.moveRight = True       
            self.rect.move_ip(-5, 0)  