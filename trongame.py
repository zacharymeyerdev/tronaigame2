import pygame
import sys
import random
from rl_agent import QLearningAgent

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

# Define the number of states and actions
n_states = 100  # This is an example; adjust based on your state representation
n_actions = 4   # UP, DOWN, LEFT, RIGHT

# Instantiate the QLearningAgent
q_learning_agent = QLearningAgent(n_states, n_actions)

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tron Game")
clock = pygame.time.Clock()
def play_step(action):
    global game_over
    # Apply the action to the game and return the reward and game_over status
    reward = 0.01
    game_over = True
    return reward, game_over

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

def reset_game():
    # Reset the game state to its initial conditions
    global player_pos, enemy_pos, player_trail, enemy_trail, game_over
    player_pos = [width//4, height//2]
    enemy_pos = [3*width//4, height//2]
    player_trail = []
    enemy_trail = []
    game_over = False
    # Any other necessary resets

def get_current_state():
    # Transform the game state into a format suitable for the RL agent
    # This might include positions of players, direction, etc.
    state = 4
    return state

# Assuming number_of_episodes is defined
number_of_episodes = 1000

def train_ai():
    global game_over
    for episode in range(number_of_episodes):
        reset_game()
        state = get_current_state()
        while not game_over:
            action = q_learning_agent.choose_action(state)
            reward, game_over = perform_action(action)
            new_state = get_current_state()
            q_learning_agent.learn(state, action, reward, new_state)
            state = new_state
        print(f"Episode {episode + 1} completed")

def perform_action(action):
    global player_pos, enemy_pos, game_over, player_trail, enemy_trail
    # Apply the action to the game
    # Update the game state based on the action
    # For example, move the player, update the trails, etc.
    # Calculate the reward
    reward = 0.01  # Modify this based on your game's logic
    game_over = check_collisions()  # Check if the game is over after this action
    return reward, game_over

def game_loop(training_mode=False):
    global player_pos, enemy_pos, player_trail, enemy_trail, player_direction, enemy_direction, game_over

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not training_mode:
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
        else:
            # Update AI (Enemy) in Training Mode
            state = get_current_state()
            action = q_learning_agent.choose_action(state)
            reward, game_over = perform_action(action)
            new_state = get_current_state()
            q_learning_agent.learn(state, action, reward, new_state)

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
            if training_mode:
                # Reset the game for the next training episode
                reset_game()
                game_over = False
            else:
                break  # End the game in playing mode

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

def play_game_with_agent(agent):
    reset_game()  # Reset the game to the initial state
    state = get_current_state()  # Get the initial state

    while not game_over:
        action = agent.choose_action(state)
        reward = perform_action(action)  # Perform the action and get the reward
        new_state = get_current_state()  # Get the new state after the action

        agent.learn(state, action, reward, new_state)  # Agent learns from the action

        state = new_state  # Update the state for the next iteration

# Game loop
for episode in range(number_of_episodes):
    play_game_with_agent(q_learning_agent)

# After training
train_ai()  # Comment this out after training is done

# To play the game
#game_loop()  # Uncomment this to play the game
