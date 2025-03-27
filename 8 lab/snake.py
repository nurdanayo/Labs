import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Epic Snake Adventure")

# Snake setup
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body
snake_dir = (CELL_SIZE, 0)  # Moving right initially

# Walls - Adding some internal obstacles
def generate_walls():
    walls = [(x, 0) for x in range(0, WIDTH, CELL_SIZE)] + [(x, HEIGHT - CELL_SIZE) for x in range(0, WIDTH, CELL_SIZE)] + \
            [(0, y) for y in range(0, HEIGHT, CELL_SIZE)] + [(WIDTH - CELL_SIZE, y) for y in range(0, HEIGHT, CELL_SIZE)]
    for _ in range(10):  # Random obstacles
        walls.append((random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE,
                      random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE))
    return walls

walls = generate_walls()

# Function to generate food avoiding walls and snake
def generate_food():
    while True:
        x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
        y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)

# Food setup
food = generate_food()

# Game variables
score = 0
level = 1
speed = 100  # Lower value = faster movement
font = pygame.font.Font(None, 36)

def draw_snake():
    for i, segment in enumerate(snake):
        color = GREEN if i > 0 else YELLOW  # Head is yellow
        pygame.draw.rect(screen, color, (*segment, CELL_SIZE, CELL_SIZE))

# Game loop
running = True
while running:
    pygame.time.delay(speed)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Snake movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)
    if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)
    
    # Move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Check collision with walls
    if new_head in walls or new_head in snake:
        running = False  # Game over if colliding with wall or itself
    
    # Check if food is eaten
    if new_head == food:
        score += 1
        snake.append(snake[-1])  # Grow snake
        food = generate_food()
        
        # Level progression
        if score % 3 == 0:
            level += 1
            speed = max(50, speed - 10)  # Increase speed (but not too fast)
            walls = generate_walls()  # New obstacles every level
    
    # Update snake position
    snake.insert(0, new_head)
    snake.pop()
    
    # Drawing elements
    screen.fill(WHITE)
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, BLACK, (*wall, CELL_SIZE, CELL_SIZE))
    
    # Draw snake
    draw_snake()
    
    # Draw food
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    
    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()

pygame.quit()
