# Import the pygame module
import sys
import pygame
from button import Button
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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH/2, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH/2, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH/2, 550), 
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
            
        clock.tick(30)
        pygame.display.flip()
    
if __name__ == "__main__":
    main_menu()