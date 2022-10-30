import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((width, hight))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x+width/2, y+hight/2))

def generate_maze(width, hight):
    walls = []
    walls.append(Wall(20, hight, 0, 0))
    walls.append(Wall(width, 20, 0, 0))
    walls.append(Wall(20, hight, width-20, 0))
    walls.append(Wall(width, 20, 0, hight-20))
    return walls