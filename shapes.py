from random import choice, randint
import pygame

GAP = 30

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, isWall=False, heat=0, isFinish=False):
        super(Cell, self).__init__()
        self.image = pygame.image.load("assets/Wall.jpg").convert()
        self.surf = pygame.transform.scale(self.image, (GAP, GAP))
        self.humanSurf = pygame.transform.scale(self.image, (GAP, GAP))
        self.x = x
        self.y = y
        self.isWall = isWall
        self.isFinish = isFinish
        if(not self.isWall):
            self.surf.fill((0,0,0))
            self.humanSurf.fill((0,0,0))
        self.rect = self.surf.get_rect(center=(x*GAP+GAP/2, y*GAP+GAP/2))
        self.heat = heat
        self.alien_saw_heat = False
        self.containsAlien = False
    
    def add_heat(self):
        self.heat = 255
        self.surf.fill((255, 0, 0))
        
    def reduce_heat(self):
        if self.heat > 0:
            self.heat-=3
            self.surf.fill((self.heat, 0, 0))

    def set_wall(self, isWall):
        self.isWall = isWall
        if isWall:
            self.surf = pygame.transform.scale(self.image, (GAP, GAP))
            self.humanSurf = pygame.transform.scale(self.image, (GAP, GAP))
        else:
            self.surf.fill((0,0,0))
            self.humanSurf.fill((0,0,0))

    def setAlien(self, hasAlien):
        self.containsAlien = hasAlien

    def __repr__(self):
        return f"{1 if self.isWall else 0}"
    
    def __str__(self):
        return f"{1 if self.isWall else 0}"

class CollisionTest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(CollisionTest, self).__init__()
        self.rect = pygame.Rect(x, y, 10, 10)


def gen_walls_array(screen_width, screen_hight):
    num_width = screen_width//(GAP*2)
    num_hight = screen_hight//(GAP)
    walls = [[Cell(x,y,isWall=(x == 0 or x == num_width-1 or y == 0 or y == num_hight-1)) for x in range(num_width)] for y in range(num_hight)]
    rand_top = randint(1, len(walls[0])-2)
    rand_bot = randint(1, len(walls[-1])-2)
    
    print(f"H-W: {num_hight}-{num_width}")
    gen_random_rooms(walls, num_width, num_hight, 9, 15,5)

    walls[0][rand_top].set_wall(False)
    walls[1][rand_top].set_wall(False)
    walls[-1][rand_bot].set_wall(False)
    walls[-2][rand_top].set_wall(False)

    return (walls, (rand_top, rand_bot))

def gen_walls_array_from_list(board):
    walls = []
    for y, line in enumerate(board):
        cells = []
        for x, val in enumerate(line):
            cells.append(Cell(x, y, isWall=val))
        walls.append(cells)
    walls[0][board[0].index(0)].isFinish = True
    return (walls, (board[0].index(0), board[-1].index(0)))

def gen_random_rooms(walls,num_width, num_hight, number_of_rooms, max_size, min_size=3):
    added_rooms = []
    doors = []
    
    for _ in range(number_of_rooms):
        attempts = 0
        nested_attempts = 0
        while(True):
            attempts += 1
            if attempts > 30:
                break
            should_add = True

            x1 = randint(0, num_width-min_size)
            nested_attempts = 0
            while(True):
                nested_attempts += 1
                if nested_attempts > 30:
                    x2 = x1 + 2
                    break
                x2 = randint(x1, num_width-2)
                if x2 - x1 < max_size and x2 - x1 > 2:
                    break
            y1 = randint(0, num_hight-min_size)
            if nested_attempts == 31:
                continue
            nested_attempts = 0
            while(True):
                attempts += 1
                if attempts > 30:
                    y2 = y1 + 2
                    break
                y2 = randint(y1, num_hight-2)
                if y2- y1 < max_size and y2 - y1 > 2:
                    break
            if nested_attempts == 31:
                continue

            for old_x1, old_x2, old_y1, old_y2 in added_rooms:
                if x1 > old_x1 and x1 < old_x2:
                    if y1 >= old_y1 and y1 < old_y2:
                        if x2 > old_x1 and x2 < old_x2:
                            if y2 > old_y1 and y2 < old_y2:
                                should_add = False
                                break
            if should_add:
                added_rooms.append((x1,x2,y1,y2))
                break
                
    for x1, x2, y1, y2 in added_rooms:
        if randint(0,1):
            while(True):
                rand_x = randint(x1+1,x2-1)
                rand_y = choice((y1,y2))
                if rand_x != 0 and rand_x != num_width-1 and rand_y != 0 and rand_y != num_hight-1:
                    break
            doors.append((rand_y-1, rand_x))
            doors.append((rand_y+1, rand_x))
        else:
            while(True):
                rand_x = choice((x1,x2))
                rand_y = randint(y1+1,y2-1)
                if rand_x != 0 and rand_x != num_width-1 and rand_y != 0 and rand_y != num_hight-1:
                    break
            doors.append((rand_y, rand_x-1))
            doors.append((rand_y, rand_x+1))
        doors.append((rand_y, rand_x))

        print(f"({x1}, {y1}) - ({x2}, {y2})")    
        
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                if (y == y1 or y == y2) or (x == x1 or x == x2):
                    walls[y][x].set_wall(True)
                else:
                    walls[y][x].set_wall(False)
                
    for y, x in doors:
        walls[y][x].set_wall(False)      