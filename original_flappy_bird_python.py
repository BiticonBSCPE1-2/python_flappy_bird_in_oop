import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thonny Flappy Bird")

# Load images
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (80, 50))

pipe_img = pygame.image.load("pipe.png").convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (160, 300))
flipped_pipe_img = pygame.transform.flip(pipe_img, False, True)

backgrounds = ["background1.png", "background2.png", "background3.png"]
current_bg = pygame.image.load(backgrounds[0]).convert_alpha()
current_bg = pygame.transform.scale(current_bg, (WIDTH, HEIGHT))

explosion_img = pygame.image.load("explosion.png").convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (120, 120))

# Create masks for pixel-perfect collisions
bird_mask = pygame.mask.from_surface(bird_img)
pipe_mask = pygame.mask.from_surface(pipe_img)

# Bird settings
bird_x, bird_y = 50, HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Pipe settings
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
running = True
game_started = False

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(100, 300)
    pipes.append({"x": WIDTH, "top": pipe_height, "bottom": pipe_height + pipe_gap})

# Function to reset game
def reset_game():
    global bird_y, bird_velocity, pipes, score, current_bg
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    create_pipe()
    current_bg = pygame.image.load(backgrounds[0]).convert_alpha()
    current_bg = pygame.transform.scale(current_bg, (WIDTH, HEIGHT))

# Initial pipes
create_pipe()

# Function to draw retry button
def draw_retry_button():
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 40, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), button_rect)
    retry_text = font.render("Retry", True, (255, 255, 255))
    screen.blit(retry_text, (WIDTH // 2 - 25, HEIGHT // 2 + 50))
    return button_rect

# Function to check for exact collision using masks
def check_collision(bird_x, bird_y, pipes):
    bird_mask = pygame.mask.from_surface(bird_img)  # Update bird mask
    for pipe in pipes:
        pipe_x, pipe_top_y = pipe["x"], pipe["top"] - 300
        pipe_bottom_y = pipe["bottom"]

        # Create masks for pipes
        pipe_top_mask = pygame.mask.from_surface(pipe_img)
        pipe_bottom_mask = pygame.mask.from_surface(pipe_img)

        # Calculate offsets (distance between bird and pipes)
        top_offset = (pipe_x - bird_x, pipe_top_y - bird_y)
        bottom_offset = (pipe_x - bird_x, pipe_bottom_y - bird_y)

        # Check pixel-perfect collision
        if bird_mask.overlap(pipe_top_mask, top_offset) or bird_mask.overlap(pipe_bottom_mask, bottom_offset):
            return True

    return False

# Game loop
while running:
    screen.blit(current_bg, (0, 0))  # Draw background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
                bird_velocity = jump_strength  # Bird jumps

    if game_started:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        for pipe in pipes:
            pipe["x"] -= pipe_velocity

        # Add new pipes & remove old ones
        if pipes[-1]["x"] < WIDTH - 200:
            create_pipe()
        if pipes[0]["x"] < -pipe_width:
            pipes.pop(0)
            score += 1  # Score increases when passing a pipe

        # Change background dynamically
        if score >= 5:
            current_bg = pygame.image.load(backgrounds[1]).convert_alpha()
            current_bg = pygame.transform.scale(current_bg, (WIDTH, HEIGHT))
        if score >= 10:
            current_bg = pygame.image.load(backgrounds[2]).convert_alpha()
            current_bg = pygame.transform.scale(current_bg, (WIDTH, HEIGHT))

        # Collision detection using pixel-perfect hitbox
        game_over = check_collision(bird_x, bird_y, pipes)

        # Check if bird hits the ground
        if bird_y > HEIGHT:
            game_over = True

        # Draw pipes
        for pipe in pipes:
            screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe["x"], pipe["top"] - 300))  # Top pipe
            screen.blit(pipe_img, (pipe["x"], pipe["bottom"]))  # Bottom pipe

        # Draw bird
        screen.blit(bird_img, (bird_x, int(bird_y)))

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # If game over, show explosion & retry button
        if game_over:
            screen.blit(explosion_img, (bird_x - 10, bird_y - 10))  # Explosion effect
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))

            retry_button = draw_retry_button()  # Draw retry button
            pygame.display.flip()  # Update screen

            # Wait for retry click
            retry_clicked = False
            while not retry_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        retry_clicked = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if retry_button.collidepoint(event.pos):
                            reset_game()
                            retry_clicked = True
                            game_started = False  # Restart game from the beginning

    else:
        # Show start message before game starts
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()

