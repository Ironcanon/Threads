import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

class Alien(pygame.sprite.Sprite):
    def __init__(self, start):
        size = 30
        super(Alien, self).__init__()
        image = pygame.image.load("assets/Alien.png").convert()
        self.surf = pygame.transform.scale(image, (size, size))
        self.replaceSurf = pygame.Surface((size, size))
        self.replaceSurf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(start)

        self.moveUp = True
        self.moveDown = True
        self.moveLeft = True
        self.moveRight = True
        self.currentCell = None

    def update(self, keysPressed, SCREEN_WIDTH, SCREEN_HEIGHT, wallGroup, alienScreen, cells):
        moveMade = False
        if keysPressed[K_UP] and self.moveUp:
            alienScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(0, -5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_DOWN] and self.moveDown:
            alienScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(0, 5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_LEFT] and self.moveLeft:
            alienScreen.blit(self.replaceSurf, self.rect)            
            self.rect.move_ip(-5, 0)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_RIGHT] and self.moveRight:
            alienScreen.blit(self.replaceSurf, self.rect)
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

        alienScreen.blit(self.surf, self.rect)

        if moveMade:
            if (self.currentCell != None):
                self.currentCell.setAlien(False)
            self.currentCell = pygame.sprite.spritecollideany(self, cells)
            self.currentCell.setAlien(True)


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