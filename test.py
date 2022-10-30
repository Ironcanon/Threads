# Import the pygame module
import pygame
from shapes import generate_maze, gen_walls_array

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

print(gen_walls_array(SCREEN_WIDTH, SCREEN_HEIGHT))

canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Camera rectangles for sections of  the canvas
p1_camera = pygame.Rect(0,0,SCREEN_WIDTH/2,SCREEN_HEIGHT)
p2_camera = pygame.Rect(SCREEN_WIDTH/2,0,SCREEN_WIDTH/2,SCREEN_HEIGHT)


# subsurfaces of canvas
# Note that subx needs refreshing when px_camera changes.
human_screen = canvas.subsurface(p1_camera)
alien_screen = canvas.subsurface(p2_camera)

# pygame.draw.line(alien_screen, (255,255,255), (0,0), (0,SCREEN_HEIGHT), 10)

screens = [human_screen, alien_screen]

screen.fill((0, 0, 0))

board = gen_walls_array(SCREEN_WIDTH, SCREEN_HEIGHT)
print(board)
walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
dirty_sprites = pygame.sprite.Group()

for row in board:
    for cell in row:
        if cell.isWall:
            walls.add(cell)
        all_sprites.add(cell)

for sub_screen in screens:
    # for wall in generate_maze(sub_screen.get_width(), sub_screen.get_height()):
    #     all_sprites.add(wall)

    for entity in all_sprites:
        sub_screen.blit(entity.surf, entity.rect)

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

    pygame.display.flip()