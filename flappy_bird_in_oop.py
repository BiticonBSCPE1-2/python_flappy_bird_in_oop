import pygame
import random

# define a class for the Flappy Bird game
class FlappyBirdGame:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # set screen width and height
        self.WIDTH, self.HEIGHT = 400, 600

        # create the screen and set caption
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Thonny Flappy Bird")

        # load and scale bird image
        self.bird_img = pygame.transform.scale(pygame.image.load("bird.png").convert_alpha(), (80, 50))

        # load and scale pipe image and its flipped version
        self.pipe_img = pygame.transform.scale(pygame.image.load("pipe.png").convert_alpha(), (160, 300))
        self.flipped_pipe_img = pygame.transform.flip(self.pipe_img, False, True)

        # load background images and set initial background
        self.backgrounds = ["background1.png", "background2.png", "background3.png"]
        self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[0]).convert_alpha(), (self.WIDTH, self.HEIGHT))

        # load and scale explosion image
        self.explosion_img = pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (120, 120))

        # create masks for collision detection
        self.bird_mask = pygame.mask.from_surface(self.bird_img)
        self.pipe_mask = pygame.mask.from_surface(self.pipe_img)

        # initialize bird position and physics
        self.bird_x = 50
        self.bird_y = self.HEIGHT // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8

        # initialize pipe settings and list
        self.pipe_width = 60
        self.pipe_gap = 150
        self.pipe_velocity = 3
        self.pipes = []

        # initialize score and font
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # set up clock and control flags
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False

        # create initial pipe
        self.create_pipe()
        
# define function to create a pipe with random height
# define function to reset the game state
# define function to draw retry button and return its rectangle
# define function to check collision using pixel-perfect masks
# create the first pipe
# start game loop
# draw background
# handle quit and spacebar press
# if game started
# apply gravity and update bird position
# move all pipes leftward
# add new pipe if needed
# remove old pipe and increase score
# change background based on score
# check for collision with pipes or ground
# draw all pipes
# draw bird
# draw score on screen
# if game over
# show explosion and game over text
# draw retry button and wait for click
# if game not started
# show "Press SPACE to Start" message
# update screen
# limit frame rate to 30 FPS
# quit pygame after loop ends
