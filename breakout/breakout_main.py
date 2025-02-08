import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
RED    = (255, 0, 0)

# Brick settings
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
brick_padding = 5
brick_offset_top = 50
brick_offset_left = 35

# List of brick color sets for each level
brick_colors = [
    (0, 255, 0),    # Level 1: Green
    (255, 255, 0),  # Level 2: Yellow
    (255, 165, 0),  # Level 3: Orange
    (255, 0, 0),    # Level 4: Red
    (0, 0, 255),    # Level 5: Blue
    (128, 0, 128)   # Level 6: Purple
]

# Paddle settings
# paddle_width = 1000 # Paddle Cheat
paddle_width = 100
paddle_height = 15
paddle_speed = 7
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)

# Ball settings
ball_radius = 10
initial_ball_speed = 4  # Base speed for ball; will scale with level
ball_speed_x = initial_ball_speed * random.choice((1, -1))
ball_speed_y = -initial_ball_speed
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Functions to create the bricks layout
def create_bricks():
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = brick_offset_left + col * (brick_width + brick_padding)
            brick_y = brick_offset_top + row * (brick_height + brick_padding)
            brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            bricks.append(brick)
    return bricks

bricks = create_bricks()

# Score, Lives, Level, and Extra Life Threshold
score = 0
lives = 3
level = 1
next_life_score = 200

# Font for text
font = pygame.font.SysFont("Arial", 24)

def draw():
    screen.fill(BLACK)
    # Draw the paddle
    pygame.draw.rect(screen, BLUE, paddle)
    # Draw the ball
    pygame.draw.circle(screen, WHITE, ball.center, ball_radius)
    # Draw bricks in the current level's color
    current_brick_color = brick_colors[(level - 1) % len(brick_colors)]
    for brick in bricks:
        pygame.draw.rect(screen, current_brick_color, brick)
    # Draw Score, Lives, and Level
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(lives), True, WHITE)
    level_text = font.render("Level: " + str(level), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    pygame.display.flip()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    # Scale ball speed with the level (increase difficulty)
    ball_speed_x = initial_ball_speed * random.choice((1, -1)) * (1.1 ** (level - 1))
    ball_speed_y = -initial_ball_speed * (1.1 ** (level - 1))

def game_over():
    over_text = font.render("Game Over!", True, RED)
    screen.blit(over_text, (WIDTH // 2 - 60, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement (using arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Move the ball
    ball.x += int(ball_speed_x)
    ball.y += int(ball_speed_y)

    # Ball collision with left/right walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    # Ball collision with top wall
    if ball.top <= 0:
        ball_speed_y *= -1

    # Ball collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    # Ball goes off the bottom: lose a life
    if ball.bottom >= HEIGHT:
        lives -= 1
        if lives <= 0:
            game_over()
        else:
            reset_ball()

    # Ball collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        bricks.pop(hit_index)
        ball_speed_y *= -1
        score += 1
        # Award an extra life every 200 points
        if score >= next_life_score:
            lives += 1
            next_life_score += 200

    # Check if level is complete (all bricks cleared)
    if len(bricks) == 0:
        level += 1
        # Increase difficulty: speed up the ball and the paddle slightly
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        paddle_speed += 1
        # Recreate the bricks (new color set will be used in draw())
        bricks = create_bricks()
        reset_ball()

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()
