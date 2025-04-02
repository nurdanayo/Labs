import pygame, math

pygame.init()

def main():
    res = w, h = 1080, 720
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()

    # Цвета
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    color = BLUE
    List = [RED, GREEN, BLUE]
    
    font = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 20)

    # Флаги для рисования
    drawrect = 0
    drawcircle = 0
    drawsquare = 0
    drawRightTriangle = 0
    drawEquilTriangle = 0
    drawRhombus = 0

    isPressed = False
    c = 0
    x = y = 0

    screen.fill(WHITE)
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            # Выход
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_w] and ctrl_held) or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and alt_held):
                return

            # Смена цвета
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = RED
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_b:
                    color = BLUE

                # Установка режима рисования
                elif event.key == pygame.K_SPACE:
                    drawrect = 1
                elif event.key == pygame.K_c:
                    drawcircle = 1
                elif event.key == pygame.K_s:
                    drawsquare = 1
                elif event.key == pygame.K_t:
                    drawRightTriangle = 1
                elif event.key == pygame.K_y:
                    drawEquilTriangle = 1
                elif event.key == pygame.K_u:
                    drawRhombus = 1

            # Нажатие мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Переключение цвета
                if 1030 <= x <= 1045 and 40 <= y <= 55:
                    if c > 2:
                        c = 0
                    color = List[c]
                    c += 1
                # Ластик
                elif 1030 <= x <= 1045 and 1 <= y <= 16:
                    color = WHITE
                isPressed = True

            # Отпустили кнопку мыши
            elif event.type == pygame.MOUSEBUTTONUP:
                isPressed = False

            # Рисование мышью
            if event.type == pygame.MOUSEMOTION and isPressed and not any([drawrect, drawcircle, drawsquare, drawRightTriangle, drawEquilTriangle, drawRhombus]):
                x, y = pygame.mouse.get_pos()
                if color == WHITE:
                    pygame.draw.rect(screen, color, (x - 20, y - 20, 40, 40))
                else:
                    pygame.draw.circle(screen, color, (x, y), 10)

            # Рисуем прямоугольник
            if isPressed and drawrect:
                x, y = pygame.mouse.get_pos()
                pygame.draw.rect(screen, color, (x - 25, y - 20, 50, 40))
                drawrect = 0

            # Рисуем круг
            elif isPressed and drawcircle:
                x, y = pygame.mouse.get_pos()
                pygame.draw.circle(screen, color, (x, y), 20)
                drawcircle = 0

            # Рисуем квадрат
            elif isPressed and drawsquare:
                x, y = pygame.mouse.get_pos()
                pygame.draw.rect(screen, color, (x - 25, y - 25, 50, 50))
                drawsquare = 0

            # Рисуем прямоугольный треугольник
            elif isPressed and drawRightTriangle:
                x, y = pygame.mouse.get_pos()
                pygame.draw.polygon(screen, color, [(x, y), (x, y - 100), (x + 100, y)])
                drawRightTriangle = 0

            # Рисуем равносторонний треугольник
            elif isPressed and drawEquilTriangle:
                x, y = pygame.mouse.get_pos()
                height = int(100 * math.sqrt(3) / 2)
                pygame.draw.polygon(screen, color, [(x, y), (x + 100, y), (x + 50, y - height)])
                drawEquilTriangle = 0

            # Рисуем ромб
            elif isPressed and drawRhombus:
                x, y = pygame.mouse.get_pos()
                pygame.draw.polygon(screen, color, [(x, y - 60), (x + 50, y), (x, y + 60), (x - 50, y)])
                drawRhombus = 0

        # Маленький интерфейс
        pygame.draw.rect(screen, BLACK, (1030, 1, 15, 15), 1)
        eraser = font_small.render("Eraser (press me): ", True, BLACK)
        screen.blit(eraser, (833, -6))

        pygame.draw.rect(screen, color, (1030, 40, 15, 15))
        pygame.draw.rect(screen, BLACK, (1028, 38, 17, 17), 2)
        col = font_small.render("Color: ", True, BLACK)
        screen.blit(col, (960, 30))

        pygame.display.flip()
        clock.tick(60)

main()
