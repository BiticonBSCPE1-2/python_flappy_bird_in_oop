import pygame
import random

# create a base class for general game setup (Inheritance)
class BaseGame:
    def __init__(self, width, height, title):  # (Inheritance)
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

# define a class for the Flappy Bird game (Encapsulation, Inheritance)
class FlappyBirdGame(BaseGame):  # (Inheritance)
    def __init__(self):
        super().__init__(400, 600, "Thonny Flappy Bird")  # (Inheritance)

        # load and scale bird image
        self.bird_img = pygame.transform.scale(pygame.image.load("bird.png").convert_alpha(), (80, 50))  # (Polymorphism)

        # load and scale pipe image and its flipped version
        self.pipe_img = pygame.transform.scale(pygame.image.load("pipe.png").convert_alpha(), (160, 300))  # (Polymorphism)
        self.flipped_pipe_img = pygame.transform.flip(self.pipe_img, False, True)  # (Polymorphism)

        # load background images and set initial background
        self.backgrounds = ["background1.png", "background2.png", "background3.png"]
        self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[0]).convert_alpha(), (self.WIDTH, self.HEIGHT))  # (Polymorphism)

        # load and scale explosion image
        self.explosion_img = pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (120, 120))  # (Polymorphism)

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

        # set control flags
        self.running = True
        self.game_started = False

        # create initial pipe
        self.create_pipe()

# define function to create a pipe with random height (Encapsulation)
    def create_pipe(self):
        pipe_height = random.randint(100, 300)
        self.pipes.append({"x": self.WIDTH, "top": pipe_height, "bottom": pipe_height + self.pipe_gap})

# define function to reset the game state (Encapsulation)
    def reset_game(self):
        self.bird_y = self.HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.create_pipe()
        self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[0]).convert_alpha(), (self.WIDTH, self.HEIGHT))

# define function to draw retry button and return its rectangle (Encapsulation)
    def draw_retry_button(self):
        button_rect = pygame.Rect(self.WIDTH // 2 - 50, self.HEIGHT // 2 + 40, 100, 40)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
        retry_text = self.font.render("Retry", True, (255, 255, 255))  # (Polymorphism)
        self.screen.blit(retry_text, (self.WIDTH // 2 - 25, self.HEIGHT // 2 + 50))
        return button_rect

# define function to check collision using pixel-perfect masks (Encapsulation, Polymorphism)
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

            if bird_mask.overlap(pipe_top_mask, top_offset) or bird_mask.overlap(pipe_bottom_mask, bottom_offset):  # (Polymorphism)
                return True
        return False

# start game loop (Encapsulation)
    def run(self):
        while self.running:

            # draw background
            self.screen.blit(self.current_bg, (0, 0))

            # handle quit and spacebar press
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_started = True
                    self.bird_velocity = self.jump_strength

            # if game started
            if self.game_started:
                # apply gravity and update bird position
                self.bird_velocity += self.gravity
                self.bird_y += self.bird_velocity

                # move all pipes leftward
                for pipe in self.pipes:
                    pipe["x"] -= self.pipe_velocity

                # add a new pipe if the last one has moved far enough
                if self.pipes and self.pipes[-1]["x"] < self.WIDTH - 200:
                    self.create_pipe()

                # remove old pipe and increase score
                if self.pipes and self.pipes[0]["x"] < -self.pipe_width:
                    self.pipes.pop(0)
                    self.score += 1

                # change background based on score
                if self.score >= 5:
                    self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[1]).convert_alpha(), (self.WIDTH, self.HEIGHT))  # (Polymorphism)
                if self.score >= 10:
                    self.current_bg = pygame.transform.scale(pygame.image.load(self.backgrounds[2]).convert_alpha(), (self.WIDTH, self.HEIGHT))  # (Polymorphism)

                # check for collision with pipes or ground
                game_over = self.check_collision() or self.bird_y > self.HEIGHT

                # draw all pipes
                for pipe in self.pipes:
                    self.screen.blit(self.flipped_pipe_img, (pipe["x"], pipe["top"] - 300))
                    self.screen.blit(self.pipe_img, (pipe["x"], pipe["bottom"]))

                # draw bird
                self.screen.blit(self.bird_img, (self.bird_x, int(self.bird_y)))

                # draw score on screen
                score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))

                # if game over
                if game_over:
                    # show explosion and game over text
                    self.screen.blit(self.explosion_img, (self.bird_x - 10, self.bird_y - 10))
                    game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
                    self.screen.blit(game_over_text, (self.WIDTH // 2 - 60, self.HEIGHT // 2 - 20))

                    # draw retry button and wait for user input
                    retry_button = self.draw_retry_button()
                    pygame.display.flip()

                    retry_clicked = False
                    while not retry_clicked:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.running = False
                                retry_clicked = True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if retry_button.collidepoint(event.pos):
                                    self.reset_game()
                                    self.game_started = False
                                    retry_clicked = True
            else:
                # show "Press SPACE to Start"
                start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))
                self.screen.blit(start_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))

            # update screen
            pygame.display.flip()

            # set frame rate to 30 FPS
            self.clock.tick(30)

        # quit pygame after exiting loop
        pygame.quit()

# run the game (Encapsulation)
if __name__ == "__main__":
    game = FlappyBirdGame()  # (Inheritance)
    game.run()
