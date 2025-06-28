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
    def create_pipe(self):
        pipe_height = random.randint(100, 300)
        self.pipes.append({"x": self.WIDTH, "top": pipe_height, "bottom": pipe_height + self.pipe_gap})

# define function to reset the game state
    def reset_game(self):
        self.bird_y = self.HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.create_pipe()
        self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[0]).convert_alpha(), (self.WIDTH, self.HEIGHT))
        
# define function to draw retry button and return its rectangle
    def draw_retry_button(self):
        button_rect = pygame.Rect(self.WIDTH // 2 - 50, self.HEIGHT // 2 + 40, 100, 40)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
        retry_text = self.font.render("Retry", True, (255, 255, 255))
        self.screen.blit(retry_text, (self.WIDTH // 2 - 25, self.HEIGHT // 2 + 50))
        return button_rect
    
# define function to check collision using pixel-perfect masks
    def check_collision(self):
        bird_mask = pygame.mask.from_surface(self.bird_img)
        for pipe in self.pipes:
            pipe_x = pipe["x"]
            pipe_top_y = pipe["top"] - 300
            pipe_bottom_y = pipe["bottom"]

            pipe_top_mask = pygame.mask.from_surface(self.pipe_img)
            pipe_bottom_mask = pygame.mask.from_surface(self.pipe_img)

            top_offset = (pipe_x - self.bird_x, pipe_top_y - int(self.bird_y))
            bottom_offset = (pipe_x - self.bird_x, pipe_bottom_y - int(self.bird_y))

            if bird_mask.overlap(pipe_top_mask, top_offset) or bird_mask.overlap(pipe_bottom_mask, bottom_offset):
                return True
        return False
    
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
