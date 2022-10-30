import pygame

GAP = 20

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y,colour=(255,255,255)):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((width, hight))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x+width/2, y+hight/2))

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, isWall=False, heat=0):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((GAP, GAP))
        self.surf.fill((255,255,255) if isWall else (0,0,0))
        self.rect = self.surf.get_rect(center=(x+GAP/2, y+GAP/2))

def generate_maze(width, hight):
    walls = []
    # Edge walls
    walls.append(Wall(GAP, hight, 0, 0))
    walls.append(Wall(width, GAP, 0, 0))
    walls.append(Wall(GAP, hight, width-GAP, 0))
    walls.append(Wall(width, GAP, 0, hight-GAP))

    walls.extend(room(0,0,14*GAP,8*GAP,12*GAP,7*GAP))
    walls.extend(room(2*GAP,10*GAP,8*GAP,18*GAP,3*GAP,17*GAP))
    walls.extend(room(2*GAP,10*GAP,8*GAP,18*GAP,3*GAP,17*GAP))
    walls.extend(room(10*GAP,10*GAP,16*GAP,18*GAP,11*GAP,17*GAP))
    walls.extend(room(18*GAP,10*GAP,width,18*GAP,19*GAP,17*GAP))
    walls.append(Wall(GAP*2, GAP*2, 22*GAP, 13*GAP))
    walls.append(Wall(GAP*2, GAP*2, 26*GAP, 13*GAP))
    walls.append(Wall(GAP*2, GAP*2, 30*GAP, 13*GAP))
    walls.append(Wall(GAP*2, GAP*2, 34*GAP, 13*GAP))
    walls.append(Wall(GAP*2, GAP*2, 38*GAP, 13*GAP))
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

def gen_walls_array(screen_width, screen_hight):
    num_width = screen_width//(GAP*2)
    num_hight = screen_hight//(GAP)
    walls = [[Cell(x,y,isWall=(x == 0 or x == num_width-1 or y == 0 or y == num_hight-1)) for x in range(num_width)] for y in range(num_hight)]
    print(walls)