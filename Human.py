# Import the pygame module
import math
import pygame

from pygame.locals import (
    K_a,
    K_s,
    K_d,
    K_w,
    K_SPACE,
    K_LSHIFT
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
        self.bodyTemperature = 150
        self.stamina = 500
        self.tired = False
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

        moveSpeed = 5

        if current_cell != None:
            # Check if at the exit
            if current_cell.isFinish:
                self.win = True
                return
            # If human is cold decrease cold time
            # Else make the current tile hot
            if self.cold_time == 0:
                current_cell.add_heat(self.bodyTemperature)
                heatedCells.add(current_cell)
                if self.bodyTemperature > 150:
                    self.bodyTemperature -= 1
            else:
                self.cold_time -= 1

        upMove = False
        downMove = False
        leftMove = False
        rightMove = False
        sprinting = False

        if (not self.tired) and self.stamina > 0 and (keys_pressed[K_LSHIFT]):
            sprinting = True
            moveSpeed = 8
            self.bodyTemperature += 3
            if self.bodyTemperature > 255:
                self.bodyTemperature = 255

        # Move the human one step at a time
        for step in range(0, moveSpeed):
            if keys_pressed[K_w]:
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(0, -1)
                upMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(0, 1)
                    upMove = False
            if keys_pressed[K_s]:
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(0, 1)
                downMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(0, -1)
                    downMove = False
            if keys_pressed[K_a]:
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(-1, 0)
                leftMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(1, 0)
                    leftMove = False
            if keys_pressed[K_d]:
                human_screen.blit(self.replace_surf, self.rect)
                self.rect.move_ip(1, 0)
                rightMove = True
                if pygame.sprite.spritecollideany(self, wall_group):
                    self.rect.move_ip(-1, 0)
                    rightMove = False

            if moveMade == False:
                if upMove or downMove or leftMove or rightMove:
                    moveMade = True

        if keys_pressed[K_SPACE] and self.item == "extinguisher":
            self.item == "None"
            self.cold_time = 1000

        if moveMade and sprinting:
            self.stamina -= 10
            if self.stamina <= 0:
                self.tired = True
        elif moveMade:
            self.stamina += 1
            if self.stamina > 200:
                self.tired = False
                if self.stamina > 500:
                    self.stamina = 500
        elif not moveMade:
            self.stamina += 3
            if self.stamina > 200:
                self.tired = False
                if self.stamina > 500:
                    self.stamina = 500

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