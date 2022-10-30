# Import the pygame module
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((75, 72))
        self.surf.fill((255, 0, 0))
        self.rect = self.rect.get_rect()