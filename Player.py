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

    def update(self, keysPressed, SCREEN_WIDTH, SCREEN_HEIGHT, wallGroup):
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

        collidedSprite = pygame.sprite.spritecollideany(self, wallGroup)

        while (collidedSprite != None):

            directionDistances = []

            directionDistances.append(self.rect.bottom - collidedSprite.rect.top)
            directionDistances.append(collidedSprite.rect.bottom - self.rect.top)
            directionDistances.append(self.rect.right - collidedSprite.rect.left)
            directionDistances.append(collidedSprite.rect.right - self.rect.left)

            largestValue = directionDistances[0]
            largestDirectionIndex = 0
            equalDistance = -1

            for i in range(1, 4):
                if directionDistances[i] > largestValue:
                    largestValue = directionDistances[i]
                    largestDirectionIndex = i
                    equalDistance = -1
                elif directionDistances[i] == largestValue:
                    equalDistance = i

            if largestDirectionIndex == 0 or equalDistance == 0:
                self.rect.top = collidedSprite.rect.bottom
            if largestDirectionIndex == 1 or equalDistance == 1:
                self.rect.bottom = collidedSprite.rect.top
            if largestDirectionIndex == 2 or equalDistance == 2:
                self.rect.left = collidedSprite.rect.right
            if largestDirectionIndex == 3 or equalDistance == 3:
                self.rect.right = collidedSprite.rect.left

            collidedSprite = pygame.sprite.spritecollideany(self, wallGroup)


            

        

        
        return moveMade
