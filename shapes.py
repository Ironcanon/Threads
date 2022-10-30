import pygame

GAP = 30

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y,colour=(255,255,255)):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((width, hight))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x+width/2, y+hight/2))

def generate_maze(width, hight):
    walls = []
    # Edge walls
    walls.append(Wall(GAP, hight, 0, 0))
    walls.append(Wall(width, GAP, 0, 0))
    walls.append(Wall(GAP, hight, width-GAP, 0))
    walls.append(Wall(width, GAP, 0, hight-GAP))

    walls.extend(room(0,0,14*GAP,8*GAP,12*GAP,7*GAP))
    walls.extend(room(2*GAP,10*GAP,8*GAP,18*GAP,3*GAP,17*GAP))
    walls.extend(room(13*GAP,0,width,8*GAP,14*GAP,7*GAP))

    walls.append(Wall(GAP, GAP, GAP, hight-GAP, colour=(0,0,0)))
    walls.append(Wall(GAP, GAP, width-GAP*2, 0, colour=(0,0,0)))
    return walls

def room(x1,y1,x2,y2,door_x,door_y):
    walls = []
    # Edge walls
    walls.append(Wall(GAP, y2-y1, x1, y1))
    walls.append(Wall(x2-x1, GAP, x1, y1))
    walls.append(Wall(GAP, y2-y1, x2-GAP, y1))
    walls.append(Wall(x2-x1, GAP, x1, y2-GAP))
    walls.append(Wall(GAP, GAP, door_x, door_y, colour=(0,0,0)))
    return walls