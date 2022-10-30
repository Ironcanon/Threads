# Import the pygame module
import pygame

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

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))# Image(Surface) which will be refrenced

canvas = pygame.Surface((800, 600))

# Camera rectangles for sections of  the canvas
p1_camera = pygame.Rect(0,0,400,600)
p2_camera = pygame.Rect(400,0,400,600)

# subsurfaces of canvas
# Note that subx needs refreshing when px_camera changes.
sub1 = canvas.subsurface(p1_camera)
sub2 = canvas.subsurface(p2_camera)

# Drawing a line on each split "screen" 
pygame.draw.line(sub2, (255,255,255), (0,0), (0,600), 10)

pygame.draw.line(sub2, (0, 255, 0), (100, 100), (400, 400), 10)

# draw player 1's view  to the top left corner
screen.blit(sub1, (0,0))
# player 2's view is in the top right corner
screen.blit(sub2, (400, 0))

display = pygame.display



# Update the screen
display.update()

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
            
    # then you update the display
    # this can be done with either display.flip() or display.update(), the
    # uses of each are beyond this question
    display.update()