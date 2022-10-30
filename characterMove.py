# Import the pygame module
import pygame
from Player import Player
from Wall import Wall

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

player = Player()

# Draw the player on the screen
screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
pygame.display.flip()

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

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    if player.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT):
        screen.fill((0, 0, 0))
        screen.blit(player.surf, player.rect)

    pygame.display.flip()

