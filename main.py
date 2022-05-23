#############################################################################################################


import pygame
import os
import time
import random
pygame.font.init() # initialize the fonts


#############################################################################################################


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


#############################################################################################################


class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img, (self.x, self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0) # not on the screen

    def collision(self, obj):
        return collide(self, obj)



class Ship: # abstract class which to inherit from
    COOLDOWN = 30

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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown() # track when to send another laser
        for laser in self.lasers:
            laser.move(vel) # move laser at velocity
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) # remove laser if off screen
            elif laser.collision(obj): # check for object collision
                obj.health -= 10 # decrease object health by 10
                self.lasers.remove(laser) # remove the laser

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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

    def move_lasers(self,vel,objs):
        self.cooldown() # track when to send another laser
        for laser in self.lasers:
            laser.move(vel) # move laser at velocity
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) # remove laser if off screen
            else:
                for obj in objs:
                    if laser.collision(obj): # check for object collision
                        obj.remove(obj) # remove object of collision
                        self.lasers.remove(laser) # remove the laser

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))



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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None # (x,y)


#############################################################################################################


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
    laser_vel = 5 # speed of the lasers

    player = Player(300, 630) # Create a Ship

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
        if keys[pygame.K_w] and player.y - player_vel > 0: #upw
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # loop to move the enemies from a copy [:] of list down screen and delete
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*FPS) == 1: # per second - FPS
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)


#############################################################################################################


main()