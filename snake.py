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
            food_type = random.choice(["normal", "special", "rare"])  # Randomly choose food type
            return (x, y, food_type, pygame.time.get_ticks())  # Include time of creation for timer

# Food setup
food = generate_food()

# Game variables
score = 0
level = 1
speed = 100  # Lower value = faster movement
font = pygame.font.Font(None, 36)

# Load food images
food_images = {
    "normal": pygame.image.load("/Users/macbook/Downloads/food.png"),
    "special": pygame.image.load("/Users/macbook/Downloads/food2.png"),
    "rare": pygame.image.load("/Users/macbook/Downloads/food3.png")
}

# Load snake images
snake_head_image = pygame.image.load("/Users/macbook/Downloads/icon.png")
snake_body_image = pygame.image.load("/Users/macbook/Downloads/icon.png")

def draw_snake():
    # Draw the head of the snake
    head = snake[0]
    screen.blit(snake_head_image, (head[0], head[1]))

    # Draw the body of the snake
    for segment in snake[1:]:
        screen.blit(snake_body_image, (segment[0], segment[1]))

# Function to check if food is expired
def is_food_expired(food):
    x, y, food_type, created_at = food
    food_info = food_types[food_type]  # Corrected here to access food_types properly
    if pygame.time.get_ticks() - created_at > food_info["timer"]:  # Check if time is up
        return True
    return False

# Define food types with timer and score
food_types = {
    "normal": {"score": 1, "timer": 5000},  # 5 seconds lifespan for normal food
    "special": {"score": 3, "timer": 7000},  # 7 seconds lifespan for special food
    "rare": {"score": 5, "timer": 10000}  # 10 seconds lifespan for rare food
}

# Game over function
def game_over():
    game_over_font = pygame.font.Font(None, 48)
    game_over_text = game_over_font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

# Game loop
running = True
while running:
    pygame.time.delay(speed)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game
    
    # Check if food is expired, if so, generate new food
    if is_food_expired(food):
        food = generate_food()

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
    
    # Check collision with walls or self (Game Over)
    if new_head in walls or new_head in snake:
        game_over()  # Game over if colliding with wall or itself
    
    # Check if food is eaten
    food_x, food_y, food_type, _ = food
    if new_head == (food_x, food_y):  # This is the part where snake "eats" food
        score += food_types[food_type]["score"]  # Add score based on food type
        snake.append(snake[-1])  # Grow snake
        food = generate_food()  # Generate new food
        
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
    food_x, food_y, food_type, _ = food
    screen.blit(food_images[food_type], (food_x, food_y))  # Draw the image of food
    
    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()

# Quit pygame
pygame.quit()



