import pygame
import sys
import random

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
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)
RED    = (255, 0, 0)

# Paddle settings
paddle_width = 100
paddle_height = 15
paddle_speed = 7
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)

# Ball settings
ball_radius = 10
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = -4
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Brick settings
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
brick_padding = 5
brick_offset_top = 50
brick_offset_left = 35
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = brick_offset_left + col * (brick_width + brick_padding)
        brick_y = brick_offset_top + row * (brick_height + brick_padding)
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append(brick)

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

def draw():
    screen.fill(BLACK)
    # Draw the paddle
    pygame.draw.rect(screen, BLUE, paddle)
    # Draw the ball
    pygame.draw.circle(screen, WHITE, ball.center, ball_radius)
    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    # Draw the score
    score_text = font.render("Score: " + str(score), True, YELLOW)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 4 * random.choice((1, -1))
    ball_speed_y = -4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement (left/right)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        # Ball missed paddle; reset ball (could trigger game over here)
        reset_ball()

    # Collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    # Collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        ball_speed_y *= -1
        score += 1

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()
