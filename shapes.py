from random import choice, randint
import pygame

GAP = 20

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y,colour=(255,255,255)):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((width, hight))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(x*GAP+width/2, y*GAP+hight/2))

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, isWall=False, heat=0):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((GAP, GAP))
        self.x = x
        self.y = y
        self.isWall = isWall
        self.surf.fill((255,255,255) if isWall else (0,0,0))
        self.rect = self.surf.get_rect(center=(x*GAP+GAP/2, y*GAP+GAP/2))
        self.heat = heat
    
    def add_heat(self):
        self.heat = 255
        self.surf.fill((255, 0, 0))
        
    def reduce_heat(self):
        if self.heat > 0:
            self.heat-=1
            self.surf.fill((self.heat, 0, 0))
        
        
    def __repr__(self):
        return f"{self.rect} {self.isWall} {self.heat}\n"
    def __str__(self):
        return f"{self.x} {self.y} {self.isWall} {self.heat}"

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
    rand_top = randint(1, len(walls[0])-2)
    rand_bot = randint(1, len(walls[-1])-2)
    
    print(f"H-W: {num_hight}-{num_width}")
    gen_random_rooms(walls, num_width, num_hight, 14, 15,5)

    walls[0][rand_top].isWall = False
    walls[1][rand_top].isWall = False
    walls[-1][rand_bot].isWall = False
    walls[-2][rand_top].isWall = False

    return walls

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
                attempts += 1
                if attempts > 30:
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
                print(f"({x1},{x2}) - ({y1},{y2})")
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
            
        
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                if (y == y1 or y == y2) or (x == x1 or x == x2):
                    walls[y][x].isWall = True
                else:
                    walls[y][x].isWall = False
                
    for y, x in doors:
        walls[y][x].isWall = False
        print(f"Door - ({y},{x})")        