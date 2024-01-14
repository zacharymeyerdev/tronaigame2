import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Variables
width, height = 600, 400
player_size = 10
player_pos = [width//4, height//2]
enemy_pos = [3*width//4, height//2]
player_color = (0, 128, 255)  # Blue
enemy_color = (255, 100, 0)  # Orange
bg_color = (0, 0, 0)  # Black
player_trail = []
enemy_trail = []
player_direction = 'RIGHT'
enemy_direction = 'LEFT'
speed = 10

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tron Game")
clock = pygame.time.Clock()

def choose_ai_action():
    # Random action selector for the enemy
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def update_ai():
    global enemy_direction
    action = choose_ai_action()  # Choose the action for the AI
    enemy_direction = action     # Set the AI's direction

def draw_trails():
    for pos in player_trail:
        pygame.draw.rect(screen, player_color, (pos[0], pos[1], player_size, player_size))
    for pos in enemy_trail:
        pygame.draw.rect(screen, enemy_color, (pos[0], pos[1], player_size, player_size))

def check_collisions():
    # Check border collisions
    if player_pos[0] >= width or player_pos[0] < 0 or player_pos[1] >= height or player_pos[1] < 0:
        return True
    if enemy_pos[0] >= width or enemy_pos[0] < 0 or enemy_pos[1] >= height or enemy_pos[1] < 0:
        return True
    # Check trail collisions
    if player_pos in player_trail[:-1] or player_pos in enemy_trail:
        return True
    if enemy_pos in enemy_trail[:-1] or enemy_pos in player_trail:
        return True

    return False
        
def game_loop():
    global player_pos, enemy_pos, player_trail, enemy_trail, player_direction, enemy_direction

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player Controls (Player)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_direction != 'DOWN':
            player_direction = 'UP'
        if keys[pygame.K_DOWN] and player_direction != 'UP':
            player_direction = 'DOWN'
        if keys[pygame.K_LEFT] and player_direction != 'RIGHT':
            player_direction = 'LEFT'
        if keys[pygame.K_RIGHT] and player_direction != 'LEFT':
            player_direction = 'RIGHT'

        # Update AI (Enemy)
        update_ai()

        # Update Player and Enemy Positions
        update_positions()

        # Draw everything
        screen.fill(bg_color)
        draw_players()
        draw_trails()

        # Update the display
        pygame.display.flip()

        # Collision detection
        if check_collisions():
            break  # End the game if there's a collision

        clock.tick(10)

def update_positions():
    global player_pos, enemy_pos

    # Update Player Position
    if player_direction == 'UP':
        player_pos[1] -= speed
    elif player_direction == 'DOWN':
        player_pos[1] += speed
    elif player_direction == 'LEFT':
        player_pos[0] -= speed
    elif player_direction == 'RIGHT':
        player_pos[0] += speed

    # Update Enemy Position
    if enemy_direction == 'UP':
        enemy_pos[1] -= speed
    elif enemy_direction == 'DOWN':
        enemy_pos[1] += speed
    elif enemy_direction == 'LEFT':
        enemy_pos[0] -= speed
    elif enemy_direction == 'RIGHT':
        enemy_pos[0] += speed

    # Add the current position to the trail
    player_trail.append(list(player_pos))
    enemy_trail.append(list(enemy_pos))

def draw_players():
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, enemy_color, (enemy_pos[0], enemy_pos[1], player_size, player_size))

game_loop()