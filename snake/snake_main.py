import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Snake and food
snake_pos = [100, 50]  # Initial position of the snake
snake_body = [[100, 50], [80, 50], [60, 50]]  # Initial body (3 blocks)
food_pos = [random.randrange(1, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(1, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
food_spawn = True

# Direction variables
direction = "RIGHT"
change_to = direction

# Score
score = 0

# Function to display score
def show_score():
    font = pygame.font.Font('freesansbold.ttf', 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game over function
def game_over():
    font = pygame.font.Font('freesansbold.ttf', 50)
    game_over_text = font.render("Game Over!", True, RED)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"

    # Update direction
    direction = change_to

    # Update snake position
    if direction == "UP":
        snake_pos[1] -= BLOCK_SIZE
    if direction == "DOWN":
        snake_pos[1] += BLOCK_SIZE
    if direction == "LEFT":
        snake_pos[0] -= BLOCK_SIZE
    if direction == "RIGHT":
        snake_pos[0] += BLOCK_SIZE

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(1, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    food_spawn = True

    # Check for collisions
    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
        game_over()
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Draw everything
    screen.fill(BLACK)
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    show_score()

    # Update display
    pygame.display.update()

    # Control the frame rate
    clock.tick(15)

# Quit Pygame
pygame.quit()
