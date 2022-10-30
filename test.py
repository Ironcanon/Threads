# Import the pygame module
import pygame
from shapes import GAP, gen_walls_array, gen_walls_array_from_list
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

# print(gen_walls_array(SCREEN_WIDTH, SCREEN_HEIGHT))

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

with open("board.txt",'r') as file:
    cellList = ast.literal_eval(file.read())
    board, (start_alien, start_human) = gen_walls_array_from_list(cellList)

# board, (start_alien, start_human) = gen_walls_array(SCREEN_WIDTH, SCREEN_HEIGHT)
# with open("board.txt",'w') as file:
#     file.write(str(board))

walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
dirty_sprites = pygame.sprite.Group()
floor = pygame.sprite.Group()
heated_cells = pygame.sprite.Group()
seenCells = pygame.sprite.Group()
interactables = pygame.sprite.Group()

def screen_blit(sprite):
    human_screen.blit(sprite.humanSurf, sprite.rect)
    alien_screen.blit(sprite.surf, sprite.rect)

for row in board:
    for cell in row:
        if cell.isWall:
            walls.add(cell)
        else:
            floor.add(cell)
                
        all_sprites.add(cell)

for entity in all_sprites:
    screen_blit(entity)

alienPlayer = Alien((GAP*start_alien, 0))
humanPlayer = Human((GAP*start_human, SCREEN_HEIGHT))
all_sprites.add(alienPlayer)
all_sprites.add(humanPlayer)

screens[0].blit(humanPlayer.surf, humanPlayer.rect)
screens[1].blit(alienPlayer.surf, alienPlayer.rect)

# draw player 1's view  to the top left corner
screen.blit(human_screen, (0,0))
# player 2's view is in the top right corner
screen.blit(alien_screen, (SCREEN_WIDTH/2, 0))
# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    coldCells = []
    for cell in heated_cells:
        cell.reduce_heat()
        if cell.heat == 0:
            coldCells.append(cell)
        screen_blit(cell)
    for currentCell in coldCells:
        heated_cells.remove(currentCell)
        
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    madeMove = False

    if humanPlayer.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT, walls, human_screen, alien_screen, floor, heated_cells, seenCells):
        madeMove = True

    if alienPlayer.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT, walls, alien_screen):
        madeMove = True
    
    if madeMove:
        screen.blit(human_screen, (0,0))
        screen.blit(alien_screen, (SCREEN_WIDTH/2, 0))
    
    # After the moves are made, check if the alien and human have collided, killing the human
    human_screen.blit(alienPlayer.surf, alienPlayer.rect)
    if pygame.sprite.collide_rect(humanPlayer, alienPlayer):
        running = False
    else:
        human_screen.blit(alienPlayer.replaceSurf, alienPlayer.rect)
        
    screen.blit(human_screen, (0,0))
    screen.blit(alien_screen, (SCREEN_WIDTH/2, 0))
        
    clock.tick(30)
    pygame.display.flip()