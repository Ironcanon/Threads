# Import the pygame module
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, startX, startY):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip((startX, startY))