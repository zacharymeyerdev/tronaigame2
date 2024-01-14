import pygame
import sys
import random
from rl_agent import QLearningAgent

# Initialize Pygame
pygame.init()

# Game Variables
width, height = 600, 400
player_size = 10
player1_pos = [width // 4, height // 2]
player2_pos = [3 * width // 4, height // 2]
player1_color = (0, 128, 255)  # Blue
player2_color = (255, 100, 0)  # Orange
bg_color = (0, 0, 0)  # Black
player1_trail = []
player2_trail = []
player1_direction = 'RIGHT'
player2_direction = 'LEFT'
speed = 10

# Instantiate two QLearningAgents
n_states = 100  # Adjust based on your game's state representation
n_actions = 4   # UP, DOWN, LEFT, RIGHT
q_learning_agent1 = QLearningAgent(n_states, n_actions)
q_learning_agent2 = QLearningAgent(n_states, n_actions)

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
    global player1_direction, player2_direction
    action1 = q_learning_agent1.choose_action(get_current_state_player1())
    action2 = q_learning_agent2.choose_action(get_current_state_player2())
    player1_direction = action1
    player2_direction = action2

def draw_trails():
    for pos in player1_trail:
        pygame.draw.rect(screen, player1_color, (pos[0], pos[1], player_size, player_size))
    for pos in player2_trail:
        pygame.draw.rect(screen, player2_color, (pos[0], pos[1], player_size, player_size))

def check_collisions_player1():
    # Check border collisions for player 1
    if player1_pos[0] >= width or player1_pos[0] < 0 or player1_pos[1] >= height or player1_pos[1] < 0:
        return True

    # Check trail collisions for player 1
    if player1_pos in player1_trail[:-1] or player1_pos in player2_trail:
        return True

    return False

def check_collisions_player2():
    # Check border collisions for player 2
    if player2_pos[0] >= width or player2_pos[0] < 0 or player2_pos[1] >= height or player2_pos[1] < 0:
        return True

    # Check trail collisions for player 2
    if player2_pos in player2_trail[:-1] or player2_pos in player1_trail:
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

def get_current_state_player1():
    # Example state representation for player 1
    state_player1 = 4
    return state_player1

def get_current_state_player2():
    # Example state representation for player 2
    state_player2 = 4
    return state_player2

def update_positions_player1():
    global player1_pos, player1_trail

    # Update Player 1 Position
    if player1_direction == 'UP':
        player1_pos[1] -= speed
    elif player1_direction == 'DOWN':
        player1_pos[1] += speed
    elif player1_direction == 'LEFT':
        player1_pos[0] -= speed
    elif player1_direction == 'RIGHT':
        player1_pos[0] += speed

    # Add the current position to Player 1's trail
    player1_trail.append(list(player1_pos))

def update_positions_player2():
    global player2_pos, player2_trail

    # Update Player 2 Position
    if player2_direction == 'UP':
        player2_pos[1] -= speed
    elif player2_direction == 'DOWN':
        player2_pos[1] += speed
    elif player2_direction == 'LEFT':
        player2_pos[0] -= speed
    elif player2_direction == 'RIGHT':
        player2_pos[0] += speed

    # Add the current position to Player 2's trail
    player2_trail.append(list(player2_pos))


def perform_action_player1(action):
    global player1_pos, player1_trail, game_over
    # Apply action for player 1
    # Update player 1 position based on action
    # Update player 1 trail
    # Calculate reward for player 1
    reward1 = 0.01
    game_over1 = check_collisions_player1()  # Check collisions for player 1
    return reward1, game_over1

def perform_action_player2(action):
    global player2_pos, player2_trail, game_over
    # Apply action for player 2
    # Update player 2 position based on action
    # Update player 2 trail
    # Calculate reward for player 2
    reward2 = 0.01
    game_over2 = check_collisions_player2()  # Check collisions for player 2
    return reward2, game_over2


# Assuming number_of_episodes is defined
number_of_episodes = 1000

def train_ai():
    global game_over
    for episode in range(number_of_episodes):
        reset_game()

        # Initial states for both agents
        state1 = get_current_state_player1()
        state2 = get_current_state_player2()

        while not game_over:
            # Agent 1 chooses an action and learns from it
            action1 = q_learning_agent1.choose_action(state1)
            reward1, game_over1 = perform_action_player1(action1)
            new_state1 = get_current_state_player1()
            q_learning_agent1.learn(state1, action1, reward1, new_state1)
            state1 = new_state1

            # Agent 2 chooses an action and learns from it
            action2 = q_learning_agent2.choose_action(state2)
            reward2, game_over2 = perform_action_player2(action2)
            new_state2 = get_current_state_player2()
            q_learning_agent2.learn(state2, action2, reward2, new_state2)
            state2 = new_state2

            # Check if the game is over for either agent
            game_over = game_over1 or game_over2
        
        print(f"Episode {episode + 1} completed")

def game_loop(training_mode=False):
    global player1_pos, player2_pos, player1_trail, player2_trail, player1_direction, player2_direction, game_over

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if training_mode:
            # Player Controls (Player 1) - Human control for demonstration
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1_direction != 'DOWN':
                player1_direction = 'UP'
            if keys[pygame.K_s] and player1_direction != 'UP':
                player1_direction = 'DOWN'
            if keys[pygame.K_a] and player1_direction != 'RIGHT':
                player1_direction = 'LEFT'
            if keys[pygame.K_d] and player1_direction != 'LEFT':
                player1_direction = 'RIGHT'

            # Player Controls (Player 2) - Human control for demonstration
            if keys[pygame.K_UP] and player2_direction != 'DOWN':
                player2_direction = 'UP'
            if keys[pygame.K_DOWN] and player2_direction != 'UP':
                player2_direction = 'DOWN'
            if keys[pygame.K_LEFT] and player2_direction != 'RIGHT':
                player2_direction = 'LEFT'
            if keys[pygame.K_RIGHT] and player2_direction != 'LEFT':
                player2_direction = 'RIGHT'
        else:
            # Update AI (Player 1) in Training Mode
            state1 = get_current_state_player1()  # Define this function based on player 1's perspective
            action1 = q_learning_agent1.choose_action(state1)
            reward1, game_over = perform_action_player1(action1) # Define this function for player 1's actions
            new_state1 = get_current_state_player1()
            q_learning_agent1.learn(state1, action1, reward1, new_state1)
                    # Update AI (Player 2) in Training Mode
        state2 = get_current_state_player2()  # Define this function based on player 2's perspective
        action2 = q_learning_agent2.choose_action(state2)
        reward2, game_over = perform_action_player2(action2)  # Define this function for player 2's actions
        new_state2 = get_current_state_player2()
        q_learning_agent2.learn(state2, action2, reward2, new_state2)

        # Update Player and Enemy Positions
        update_positions_player1()  # Define this function to update player 1's position
        update_positions_player2()  # Define this function to update player 2's position

        # Draw everything
        screen.fill(bg_color)
        draw_players()
        draw_trails()

        # Update the display
        pygame.display.flip()
        pygame.display.update()

        # Collision detection
        if check_collisions_player1 or check_collisions_player2():
            if training_mode:
                # Reset the game for the next training episode
                reset_game()
                game_over = False
            else:
                break  # End the game in playing mode

        clock.tick(10)


def update_positions():
    global player1_pos, player2_pos, player1_trail, player2_trail, player1_direction, player2_direction

    # Update Player 1 Position
    if player1_direction == 'UP':
        player1_pos[1] -= speed
    elif player1_direction == 'DOWN':
        player1_pos[1] += speed
    elif player1_direction == 'LEFT':
        player1_pos[0] -= speed
    elif player1_direction == 'RIGHT':
        player1_pos[0] += speed

    # Update Player 2 Position
    if player2_direction == 'UP':
        player2_pos[1] -= speed
    elif player2_direction == 'DOWN':
        player2_pos[1] += speed
    elif player2_direction == 'LEFT':
        player2_pos[0] -= speed
    elif player2_direction == 'RIGHT':
        player2_pos[0] += speed

    # Add the current position to the trails
    player1_trail.append(list(player1_pos))
    player2_trail.append(list(player2_pos))

def draw_players():
    pygame.draw.rect(screen, player1_color, (player1_pos[0], player1_pos[1], player_size, player_size))
    pygame.draw.rect(screen, player2_color, (player2_pos[0], player2_pos[1], player_size, player_size))

def play_game_with_agents(agent1, agent2):
    reset_game()  # Reset the game to the initial state
    state1 = get_current_state_player1()  # Define this function based on player 1's perspective
    state2 = get_current_state_player2()  # Define this function based on player 2's perspective

    while not game_over:
        # Agent 1's turn
        action1 = agent1.choose_action(state1)
        reward1 = perform_action_player1(action1)  # Define this function for player 1's actions
        new_state1 = get_current_state_player1()
        agent1.learn(state1, action1, reward1, new_state1)

        # Agent 2's turn
        action2 = agent2.choose_action(state2)
        reward2 = perform_action_player2(action2)  # Define this function for player 2's actions
        new_state2 = get_current_state_player2()
        agent2.learn(state2, action2, reward2, new_state2)

        # Update states
        state1 = new_state1
        state2 = new_state2

# Game loop for training with two agents
for episode in range(number_of_episodes):
    play_game_with_agents(q_learning_agent1, q_learning_agent2)
    print(f"Episode {episode + 1} completed")

# After training
train_ai()  # Comment this out after training is done

# To play the game
#game_loop(training_mode=True)  # Uncomment this to play the game
