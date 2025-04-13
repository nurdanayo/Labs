import pygame
import psycopg2
import random
import sys
import json

# Подключение к PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="snake_game",
    user="postgres",
    password=""  # укажи пароль, если есть
)
cursor = conn.cursor()

# Получить или создать пользователя
def get_or_create_user(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
        result = cursor.fetchone()
        level = result[0] if result else 1
        print(f"Welcome back, {username}! Starting at level {level}.")
    else:
        cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        level = 1
        print(f"Welcome, {username}! New user, starting at level 1.")
    return user_id, level

# Сохранение результата
def save_game(user_id, level, score):
    cursor.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()

# Сохранение полного состояния
def save_full_state(user_id, snake, food, direction, level, score):
    cursor.execute("""
        INSERT INTO game_state (user_id, snake, food, direction, level, score)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            snake = EXCLUDED.snake,
            food = EXCLUDED.food,
            direction = EXCLUDED.direction,
            level = EXCLUDED.level,
            score = EXCLUDED.score
    """, (
        user_id,
        json.dumps(snake),
        json.dumps(food),
        json.dumps(direction),
        level,
        score
    ))
    conn.commit()

# Загрузка состояния
def load_full_state(user_id):
    cursor.execute("SELECT snake, food, direction, level, score FROM game_state WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        snake = json.loads(result[0])
        food = tuple(json.loads(result[1]))
        direction = tuple(json.loads(result[2]))
        level = result[3]
        score = result[4]
        return snake, food, direction, level, score
    else:
        return None

# Настройки уровня
def get_level_settings(level):
    speeds = [10, 15, 20, 25]
    walls = {
        1: [],
        2: [(10, y) for y in range(5, 15)],
        3: [(x, 10) for x in range(5, 15)],
        4: [(5, y) for y in range(5, 15)] + [(15, y) for y in range(5, 15)],
    }
    return speeds[min(level - 1, len(speeds) - 1)], walls.get(level, [])

# Настройки экрана
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Save/Resume")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Цвета
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)
BLACK = (0, 0, 0)

# Запуск игры
username = input("Enter your username: ")
user_id, level = get_or_create_user(username)
initial_level = level

# Загрузка состояния
loaded = load_full_state(user_id)
if loaded:
    snake, food, direction, level, score = loaded
    head = snake[0]
    speed, walls = get_level_settings(level)
    if head in walls or not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in snake[1:]:
        print("Saved game had invalid snake position. Starting new game.")
        snake = [(5, 5)]
        direction = (1, 0)
        food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        level = 1
        score = 0
    else:
        print(f"Loaded saved game. Level {level}, Score {score}")
else:
    snake = [(5, 5)]
    direction = (1, 0)
    food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    level = 1
    score = 0

speed, walls = get_level_settings(level)
paused = False

# Игровой цикл
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(user_id, initial_level, score)
            save_full_state(user_id, snake, food, direction, level, score)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1): direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1): direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0): direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0): direction = (1, 0)
            elif event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_game(user_id, initial_level, score)
                    save_full_state(user_id, snake, food, direction, level, score)

    if paused:
        continue

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if head in snake or head in walls or not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
        print("Game Over!")
        save_game(user_id, initial_level, score)
        save_full_state(user_id, snake, food, direction, level, score)
        break

    snake.insert(0, head)
    if head == food:
        score += 10
        food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        while food in walls or food in snake:
            food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

        if score % 100 == 0:
            level += 1
            print(f"Level up! Now at level {level}")
            speed, walls = get_level_settings(level)
    else:
        snake.pop()

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for wall in walls:
        pygame.draw.rect(screen, DARK_GREEN, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)



