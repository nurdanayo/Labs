import pygame


pygame.init()


WIDTH, HEIGHT = 500, 500
BALL_RADIUS = 25  
BALL_DIAMETER = BALL_RADIUS * 2
MOVE_STEP = 20  


WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Red Ball")


ball_x = WIDTH // 2 - BALL_RADIUS
ball_y = HEIGHT // 2 - BALL_RADIUS


running = True
while running:
    screen.fill(WHITE)  
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - MOVE_STEP >= 0:
                ball_y -= MOVE_STEP
            elif event.key == pygame.K_DOWN and ball_y + MOVE_STEP + BALL_DIAMETER <= HEIGHT:
                ball_y += MOVE_STEP
            elif event.key == pygame.K_LEFT and ball_x - MOVE_STEP >= 0:
                ball_x -= MOVE_STEP
            elif event.key == pygame.K_RIGHT and ball_x + MOVE_STEP + BALL_DIAMETER <= WIDTH:
                ball_x += MOVE_STEP

    
    pygame.draw.circle(screen, RED, (ball_x + BALL_RADIUS, ball_y + BALL_RADIUS), BALL_RADIUS)
    
    
    pygame.display.flip()
    
    
    pygame.time.delay(30)


pygame.quit()