# Import the pygame module
import pygame

from pygame.locals import (
    K_a,
    K_s,
    K_d,
    K_w,
    K_SPACE
)

class Human(pygame.sprite.Sprite):
    def __init__(self, start):
        size = 29
        super(Human, self).__init__()
        image = pygame.image.load("assets/Astronaut.png").convert()
        self.surf = pygame.transform.scale(image, (size, size))
        self.replaceSurf = pygame.Surface((size, size))
        self.replaceSurf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(start)
        self.item = "None"
        self.cold_timer = 0
        self.win = False

        self.lives = 3

        self.moveUp = True
        self.moveDown = True
        self.moveLeft = True
        self.moveRight = True

    def update(self, keysPressed, SCREEN_WIDTH, SCREEN_HEIGHT, wallGroup, humanScreen, alienScreen, cells, heatedCells, seenCells):
        moveMade = False
        currentCell = pygame.sprite.spritecollideany(self, cells)
        if currentCell != None:
            if currentCell.isFinish:
                self.win = True
                return
            if self.cold_timer == 0:
                currentCell.add_heat()
                heatedCells.add(currentCell)
            else:
                self.cold_timer -= 1
            alienScreen.blit(currentCell.surf, currentCell.rect)

        if keysPressed[K_w] and self.moveUp:
            humanScreen.blit(self.replaceSurf, self.rect)
            self.rect.move_ip(0, -5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_s] and self.moveDown:
            humanScreen.blit(self.replaceSurf, self.rect)
            # alienScreen.blit(currentCell.surf, currentCell.rect)
            self.rect.move_ip(0, 5)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_a] and self.moveLeft:
            humanScreen.blit(self.replaceSurf, self.rect)
            # alienScreen.blit(currentCell.surf, currentCell.rect)
            self.rect.move_ip(-5, 0)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_d] and self.moveRight:
            humanScreen.blit(self.replaceSurf, self.rect)
            # alienScreen.blit(currentCell.surf, currentCell.rect)
            self.rect.move_ip(5, 0)
            moveMade = True
            self.checkDirections(wallGroup)
        if keysPressed[K_SPACE] and self.item == "extinguisher":
            self.item == "None"
            self.cold_timer = 1000

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

        