import pygame

MOVE_SPEED = 5

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

class Alien(pygame.sprite.Sprite):
    def __init__(self, start):
        size = 28
        super(Alien, self).__init__()
        image = pygame.image.load("assets/Alien.png").convert()
        self.surf = pygame.transform.scale(image, (size, size))
        self.replace_surf = pygame.Surface((size, size))
        self.replace_surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(start)

        self.move_up = True
        self.move_down = True
        self.move_left = True
        self.move_right = True
        self.current_cell = None

    def update(self, keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT, wall_group, alien_screen, human_screen, cells):
        
        moveMade = False
        moveSpeed = 7

        upMove = False
        downMove = False
        leftMove = False
        rightMove = False

        # Move the human one step at a time
        for step in range(0, moveSpeed):
            if keys_pressed[K_UP]:
                alien_screen.blit(self.replace_surf, self.rect)
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(0, -1)
                upMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(0, 1)
                    upMove = False
            if keys_pressed[K_DOWN]:
                alien_screen.blit(self.replace_surf, self.rect)
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(0, 1)
                downMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(0, -1)
                    downMove = False
            if keys_pressed[K_LEFT]:
                alien_screen.blit(self.replace_surf, self.rect)
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(-1, 0)
                leftMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(1, 0)
                    leftMove = False
            if keys_pressed[K_RIGHT]:
                alien_screen.blit(self.replace_surf, self.rect)
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(1, 0)
                rightMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(-1, 0)
                    rightMove = False

            if moveMade == False:
                if upMove or downMove or leftMove or rightMove:
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

        alien_screen.blit(self.surf, self.rect)

        if moveMade:
            if (self.current_cell != None):
                self.current_cell.setAlien(False)
            self.current_cell = pygame.sprite.spritecollideany(self, cells)
            self.current_cell.setAlien(True)


        return moveMade