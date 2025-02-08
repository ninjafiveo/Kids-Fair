import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 20
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))

# Paddles and ball positions
left_paddle = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Score variables
left_score = 0
right_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)
    
    # Draw the paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # Display the scores
    left_text = font.render(f"{left_score}", True, WHITE)
    right_text = font.render(f"{right_score}", True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))
    
    pygame.display.flip()

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    global ball_speed_x, ball_speed_y
    ball_speed_x = 4 * random.choice((1, -1))
    ball_speed_y = 4 * random.choice((1, -1))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top or bottom of screen
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with the paddles
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1

    # Ball goes off the screen: update score and reset ball
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

    draw()
    clock.tick(60)

pygame.quit()
