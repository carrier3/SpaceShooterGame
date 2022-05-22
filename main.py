import pygame
import os
import time
import random

# Define width and height tuple for the screen
WIDTH, HEIGHT = 750,750
# Set up the pygame window and add the predefined tuple for the screen
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# Name the display
pygame.display.set_caption("Space Shooter Game")

# Load the Enemy ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

# Load the Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

# Load the Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

# Load the background image
BG = pygame.image.load(os.path.join("assets","background-black.png"))