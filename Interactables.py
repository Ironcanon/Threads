from time import perf_counter
import pygame

class Interactable(pygame.sprite.Sprite):
    def __init__(self, where, type="None"):
        super(Interactable, self).__init__()
        self.type = type
        if (type == "egg"):
            pass
        elif (type == "extinguisher"):
            pass

        self.surf = pygame.Surface((15, 15))
        self.replace_surf = pygame.Surface((15, 15))
        self.surf.fill((0, 0, 255))
        self.replace_surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(where)
    
    def update(self, player):
        person = pygame.sprite.spritecollideany(self, player)
        if person != None:
            person.item = self.type
            self.kill()