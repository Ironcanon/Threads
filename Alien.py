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
        if keys_pressed[K_UP] and self.move_up:
            alien_screen.blit(self.replace_surf, self.rect)
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(0, -MOVE_SPEED)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_DOWN] and self.move_down:
            alien_screen.blit(self.replace_surf, self.rect)
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(0, MOVE_SPEED)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_LEFT] and self.move_left:
            alien_screen.blit(self.replace_surf, self.rect)
            human_screen.blit(self.replace_surf, self.rect)            
            self.rect.move_ip(-MOVE_SPEED, 0)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_RIGHT] and self.move_right:
            alien_screen.blit(self.replace_surf, self.rect)
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(MOVE_SPEED, 0)
            moveMade = True
            self.checkDirections(wall_group)

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

    def checkDirections(self, wall_group):
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, wall_group) != None:
                self.move_up = False
            else:
                self.move_up = True
            self.rect.move_ip(0, 10)
            if pygame.sprite.spritecollideany(self, wall_group) != None:
                self.move_down = False
            else:
                self.move_down = True
            self.rect.move_ip(-5, -5)
            if pygame.sprite.spritecollideany(self, wall_group) != None:
                self.move_left = False
            else:
                self.move_left = True
            self.rect.move_ip(10, 0)
            if pygame.sprite.spritecollideany(self, wall_group) != None:
                self.move_right = False
            else:
                self.move_right = True       
            self.rect.move_ip(-5, 0)  