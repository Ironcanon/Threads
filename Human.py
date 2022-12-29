# Import the pygame module
import math
import pygame

from pygame.locals import (
    K_a,
    K_s,
    K_d,
    K_w,
    K_SPACE
)
from shapes import GAP, Cell

class Human(pygame.sprite.Sprite):
    def __init__(self, start):
        size = 29
        super(Human, self).__init__()
        image = pygame.image.load("assets/Astronaut.png").convert()
        self.surf = pygame.transform.scale(image, (size, size))
        self.replace_surf = pygame.Surface((size, size))
        self.replace_surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(start)
        self.item = "None"
        self.cold_time = 0
        self.win = False
        self.can_see_alien = False
        self.view_dist = 15

        self.lives = 3

        self.move_up = True
        self.move_down = True
        self.move_left = True
        self.move_right = True
        self.current_cell = None

    def update(self, keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT, wall_group, human_screen, cells, heatedCells, alien):
        moveMade = False
        # Get the cell the human is currently on
        current_cell = pygame.sprite.spritecollideany(self, cells)

        if current_cell != None:
            # Check if at the exit
            if current_cell.isFinish:
                self.win = True
                return
            # If human is cold decrease cold time
            # Else make the current tile hot
            if self.cold_time == 0:
                current_cell.add_heat()
                heatedCells.add(current_cell)
            else:
                self.cold_time -= 1

        if keys_pressed[K_w] and self.move_up:
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(0, -5)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_s] and self.move_down:
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(0, 5)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_a] and self.move_left:
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(-5, 0)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_d] and self.move_right:
            human_screen.blit(self.replace_surf, self.rect)
            self.rect.move_ip(5, 0)
            moveMade = True
            self.checkDirections(wall_group)

        if keys_pressed[K_SPACE] and self.item == "extinguisher":
            self.item == "None"
            self.cold_time = 1000

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
                    
        if self.can_see_alien:
            human_screen.blit(alien.surf, alien.rect)

        human_screen.blit(self.surf, self.rect)
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