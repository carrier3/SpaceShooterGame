import pygame
import os
import time
import random
pygame.font.init() # initialize the fonts

# Define width and height tuple for the screen
WIDTH, HEIGHT = 750,750
# Set up the pygame window and add the predefined tuple for the screen
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# Name the display
pygame.display.set_caption("Space Shooter Game")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Load the background image and scale the image to the screen
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))




class Ship: # abstract class which to inherit from

    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None # allow to draw player
        self.laser_img = None # allow to draw laser
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()



class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health



class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def main():

    run = True # dictates whether te while loop runs
    FPS = 60 # how many times per second the program checks for changes such as collisions or movement. Higher FPS makes game run faster, lower FPS makes game run slower
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans",50)
    lost_font = pygame.font.SysFont("comicsans",60)

    enemies = [] # blank list of enemies
    wave_length = 5
    enemy_vel = 1 # speed of enemies
    player_vel = 5 # number of pixels to move

    player = Player(300, 650) # Create a Ship

    clock = pygame.time.Clock() # create clock

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0)) #draw te image starting at the top left corner
        # draw text that is white and calls variables
        lives_label = main_font.render(f"Lives: {lives}",1,(255,255,255))
        level_label = main_font.render(f"Level: {level}",1,(255,255,255))

        # draw labels on the screen in desired position
        WIN.blit(lives_label,(10,10)) # left upper screen
        WIN.blit(level_label,(WIDTH - level_label.get_width() - 10, 10)) # right upper screen - dynamic

        # for each enemy in the list, draw it on the screen
        for enemy in enemies:
            enemy.draw(WIN)

        # draw the player
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350)) # position text in center of screen

        pygame.display.update()

    while run:
        clock.tick(FPS) # make sure the game stays consistent on any device
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False # quit game
            else:
                continue

        # check to see if there are still enemies, if not, increase level
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # spawn the list enemies into the game randomly
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # loop through all the events that pygame knows to check if event has occurred at timeframe of FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # returns a dictionary of all the keys and tells you whether they were pressed or not at the FPS timeframe
        keys = pygame.key.get_pressed()

        # create movement based on detected keys
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: #down
            player.y += player_vel

        # loop to move the enemies from a copy [:] of list down screen and delete
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


main()