import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Asset folder setup
asset_folder = "space_invaders/assets"

# Background
background_img = pygame.image.load(os.path.join(asset_folder, "background.png"))
background_img = pygame.transform.scale(background_img, (800, 600))  # Resize to fit the screen

# Resize helper function
def load_and_resize_image(filepath, width, height):
    image = pygame.image.load(filepath)
    return pygame.transform.scale(image, (width, height))

# Player
player_img = load_and_resize_image(os.path.join(asset_folder, "player.png"), 48, 48)  # 25% smaller
player_x = 370
player_y = 500
player_x_change = 0

def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy
num_of_enemies = 5
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

for i in range(num_of_enemies):
    enemy_img.append(load_and_resize_image(os.path.join(asset_folder, "enemy.png"), 48, 48))  # 25% smaller
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Bullet
bullet_img = load_and_resize_image(os.path.join(asset_folder, "bullet.png"), 24, 24)  # 25% smaller
bullet_x = 0
bullet_y = 500
bullet_y_change = -0.7
bullet_state = "ready"

def fire_bullet(x, y):
    """Fire the bullet from the player's current position."""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 12, y + 10))

# Collision detection
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Check if the bullet hits the enemy."""
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

def show_score():
    """Display the current score on the screen."""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Game loop
running = True
while running:
    # Draw the background
    screen.blit(background_img, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keypress handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Update player position
    player_x += player_x_change
    player_x = max(0, min(player_x, 752))  # Keep player within screen bounds

    # Update enemy positions
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= 752:
            enemy_x_change[i] *= -1  # Reverse direction
            enemy_y[i] += enemy_y_change[i]

        # Check for collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 500
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        # Draw enemy
        enemy(enemy_x[i], enemy_y[i], i)

    # Update bullet position
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change

    # Reset bullet when it goes off-screen
    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = "ready"

    # Draw player and score
    player(player_x, player_y)
    show_score()

    # Update display
    pygame.display.update()
