import pygame
from pygame.locals import *

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, RED, GREEN, BLUE]
COLOR_NAMES = ["Black", "Red", "Green", "Blue"]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing App")

# Variables
current_tool = "pen"
current_color = BLACK
drawing = False
start_pos = None
canvas = pygame.Surface((WIDTH, HEIGHT - 50))
canvas.fill(WHITE)

# Toolbar setup
tool_buttons = {
    "pen": pygame.Rect(10, 10, 80, 30),
    "rectangle": pygame.Rect(100, 10, 100, 30),
    "circle": pygame.Rect(210, 10, 80, 30),
    "eraser": pygame.Rect(300, 10, 80, 30)
}
color_buttons = {COLORS[i]: pygame.Rect(400 + i * 50, 10, 40, 30) for i in range(len(COLORS))}

# Font
font = pygame.font.Font(None, 24)

def draw_toolbar():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 50))
    for tool, rect in tool_buttons.items():
        pygame.draw.rect(screen, (150, 150, 150), rect)
        text = font.render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    draw_toolbar()
    screen.blit(canvas, (0, 50))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if event.pos[1] < 50:  # Clicked on toolbar
                    for tool, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_tool = tool
                    for color, rect in color_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_color = color
                else:
                    start_pos = event.pos[0], event.pos[1] - 50
                    drawing = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                drawing = False
                end_pos = event.pos[0], event.pos[1] - 50
                if current_tool == "rectangle":
                    pygame.draw.rect(canvas, current_color, (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
                elif current_tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
        elif event.type == MOUSEMOTION:
            if drawing and current_tool == "pen":
                pygame.draw.line(canvas, current_color, start_pos, (event.pos[0], event.pos[1] - 50), 2)
                start_pos = event.pos[0], event.pos[1] - 50
            elif drawing and current_tool == "eraser":
                pygame.draw.circle(canvas, WHITE, (event.pos[0], event.pos[1] - 50), 10)
    
    pygame.display.update()

pygame.quit()
