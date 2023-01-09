# Import the pygame module
import math
import sys
from MapGenerator import MapGenerator
import pygame
from button import Button
from shapes import GAP, CollisionTest, gen_walls_array, gen_walls_array_from_list
from Alien import Alien
from Human import Human
import ast

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_KP_ENTER,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Define constants for the screen width and height
print(pygame.display.get_window_size())
SCREEN_WIDTH = pygame.display.get_window_size()[0]
SCREEN_HEIGHT = pygame.display.get_window_size()[1]

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Camera rectangles for sections of  the canvas
p1_camera = pygame.Rect(0,0,SCREEN_WIDTH/2,SCREEN_HEIGHT)
p2_camera = pygame.Rect(SCREEN_WIDTH/2,0,SCREEN_WIDTH/2,SCREEN_HEIGHT)

# subsurfaces of canvas
# Note that subx needs refreshing when px_camera changes.
human_screen = canvas.subsurface(p1_camera)
alien_screen = canvas.subsurface(p2_camera)

# pygame.draw.line(alien_screen, (255,255,255), (0,0), (0,SCREEN_HEIGHT), 10)

clock = pygame.time.Clock()

screens = [human_screen, alien_screen]

screen.fill((0, 0, 0))

# with open("board.txt",'r') as file:
#     cell_list = ast.literal_eval(file.read())
#     board, (start_alien, start_human) = gen_walls_array_from_list(cell_list)

map_gen = MapGenerator("DefaultRooms.json")
map_gen.generate(SCREEN_WIDTH, SCREEN_HEIGHT)

board = map_gen.map
start_alien = map_gen.alien_start
start_human = map_gen.human_start

# board, (start_alien, start_human) = gen_walls_array(SCREEN_WIDTH, SCREEN_HEIGHT)

# print(len(board),start_alien,start_human)

# with open("board.txt",'w') as file:
#     file.write(str(board))

walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
dirty_sprites = pygame.sprite.Group()
floor = pygame.sprite.Group()
heated_cells = pygame.sprite.Group()
seen_cells = pygame.sprite.Group()
interactables = pygame.sprite.Group()

def screen_blit(sprite):
    human_screen.blit(sprite.humanSurf, sprite.rect)
    alien_screen.blit(sprite.surf, sprite.rect)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    screen.blit(BG, (0, 0))
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ASTRO VS PRED", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pass
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

def play():
    for row in board:
        for room in row:
            for room_row in room:
                for cell in room_row:
                    if cell.isWall:
                        walls.add(cell)
                    else:
                        floor.add(cell)
                            
                    all_sprites.add(cell)
            

    for entity in all_sprites:
        screen_blit(entity)

    alien_player = Alien((GAP*start_alien[0], GAP*start_alien[1]))
    human_player = Human((GAP*start_human[0], GAP*start_human[1]))
    all_sprites.add(alien_player)
    all_sprites.add(human_player)

    screens[0].blit(human_player.surf, human_player.rect)
    screens[1].blit(alien_player.surf, alien_player.rect)

    # Draw player 1's view from the top left to middle bottom
    screen.blit(human_screen, (0,0))
    # Draw player 2's view is in the top middle to bottom right
    screen.blit(alien_screen, (SCREEN_WIDTH/2, 0))
    running = True

    yellow = pygame.Surface((10, 10))
    yellow.fill((255,233,0))
    black = pygame.Surface((10, 10))
    black.fill((0,0,0))
    sight_markers = []
    # Main loop
    while running:
        # Check for quit events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # Store any newly cold cells to remove from heated_cells
        cold_cells = []
        for cell in heated_cells:
            cell.reduce_heat()
            if cell.heat == 0:
                cold_cells.append(cell)
            # Only show the cell if the alien can see it
            # TODO: Change this such that once an alien has seen a cell keep updating it
            if math.dist([cell.x, cell.y],[alien_player.rect.x//GAP, alien_player.rect.y//GAP]) < 10:
                cell.alien_saw_heat = True

            if cell.alien_saw_heat:
                screen_blit(cell)

        # Remove all the completely cold cells from heated_cells
        for cell in cold_cells:
            cell.alien_saw_heat = False
            heated_cells.remove(cell)
            
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        either_moved = False

        # Do human updates
        if human_player.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT, walls, human_screen, floor, heated_cells, alien_player):
            either_moved = True

        # Do alien updates
        if alien_player.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT, walls, alien_screen, human_screen, floor):
            either_moved = True

        if either_moved:
            if math.dist(human_player.rect.center, alien_player.rect.center) // GAP < human_player.view_dist:
                for cell in sight_markers:
                    human_screen.blit(black, cell.rect)
                sight_markers.clear()

                for x, y in get_line(human_player.rect.center, alien_player.rect.center):
                    test_sprite = CollisionTest(x, y)
                    # test_sprite.rect.x = x
                    # test_sprite.rect.y = y
                    current_cell = pygame.sprite.spritecollideany(test_sprite, floor)

                    if current_cell:
                        human_screen.blit(yellow, current_cell.rect)
                        sight_markers.append(current_cell)

                    if pygame.sprite.spritecollideany(test_sprite, walls):
                        human_player.can_see_alien = False   
                        break
                else:
                    human_player.can_see_alien = True
            else:
                human_player.can_see_alien = False 
        
        if human_player.can_see_alien:
            human_screen.blit(alien_player.surf, alien_player.rect)
        else:
            for cell in sight_markers:
                human_screen.blit(black, cell.rect)
            sight_markers.clear()

        # if madeMove:
        screen.blit(human_screen, (0,0))
        screen.blit(alien_screen, (SCREEN_WIDTH/2, 0))
            
        if(human_player.win):
            win("Astronaut Wins!")
            return

        # After the moves are made, check if the alien and human have collided, killing the human
        human_screen.blit(alien_player.surf, alien_player.rect)
        if pygame.sprite.collide_rect(human_player, alien_player):
            win("Alien Wins!")
            return
        else:
            human_screen.blit(alien_player.replace_surf, alien_player.rect)

        clock.tick(30)
        pygame.display.flip()
    
def win(string):
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render(string, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 100))

        MENU_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH/2, 250), 
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH/2, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    
# Taken from https://iqcode.com/code/python/python-bresenham-line-algorithm
def get_line(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = GAP if y1 < y2 else - GAP
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1, GAP):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

if __name__ == "__main__":
    main_menu()