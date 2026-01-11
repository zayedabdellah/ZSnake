import pygame
import sys
import random
import os

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('ZSnake')

clock = pygame.time.Clock()

block_size = 20
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

highscore_file = 'highscore.txt'
color_file = 'last_color.txt'

def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, 'r') as f:
            return int(f.read().strip())
    return 0

def save_highscore(score):
    with open(highscore_file, 'w') as f:
        f.write(str(score))

def load_last_color():
    if os.path.exists(color_file):
        with open(color_file, 'r') as f:
            color = f.read().strip()
            if color in colors:
                return colors.index(color)
    return 0

def save_last_color(color):
    with open(color_file, 'w') as f:
        f.write(color)

highscore = load_highscore()

colors = ['green', 'red', 'blue', 'yellow']
color_map = {
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0)
}

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = small_font.render(text, True, (255,255,255))
    screen.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))
    return False

def menu():
    selected_color = load_last_color()
    while True:
        screen.fill((0,0,0))
        title = font.render("ZSnake", True, (255,255,255))
        screen.blit(title, (width//2 - title.get_width()//2, 50))
        hs_text = font.render(f"High Score: {highscore}", True, (255,255,255))
        screen.blit(hs_text, (width//2 - hs_text.get_width()//2, 100))
        color_text = small_font.render(f"Select Color: {colors[selected_color]}", True, (255,255,255))
        screen.blit(color_text, (width//2 - color_text.get_width()//2, 200))
        # Draw color preview
        pygame.draw.rect(screen, color_map[colors[selected_color]], (width//2 - 50, 230, 100, 20))
        start_button = draw_button("Start Game", width//2 - 75, 300, 150, 50, (0,128,0), (0,200,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_color = (selected_color - 1) % len(colors)
                elif event.key == pygame.K_RIGHT:
                    selected_color = (selected_color + 1) % len(colors)
                elif event.key == pygame.K_RETURN:
                    return colors[selected_color]
        if start_button:
            return colors[selected_color]
        pygame.display.flip()
        clock.tick(30)

def game(snake_color):
    snake = [(width // 2, height // 2)]
    direction = (0, -block_size)
    food = (random.randint(0, (width // block_size) - 1) * block_size, random.randint(0, (height // block_size) - 1) * block_size)
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, block_size):
                    direction = (0, -block_size)
                elif event.key == pygame.K_DOWN and direction != (0, -block_size):
                    direction = (0, block_size)
                elif event.key == pygame.K_LEFT and direction != (block_size, 0):
                    direction = (-block_size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-block_size, 0):
                    direction = (block_size, 0)
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if head in snake or head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return score
        snake.insert(0, head)
        if head == food:
            score += 1
            food = (random.randint(0, (width // block_size) - 1) * block_size, random.randint(0, (height // block_size) - 1) * block_size)
        else:
            snake.pop()
        screen.fill((0, 0, 0))
        for segment in snake:
            pygame.draw.rect(screen, snake_color, (segment[0], segment[1], block_size, block_size))
        pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], block_size, block_size))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(10)
    return score

def game_over(score):
    global highscore
    if score > highscore:
        highscore = score
        save_highscore(highscore)
    while True:
        screen.fill((0,0,0))
        go_text = font.render("Game Over", True, (255,255,255))
        screen.blit(go_text, (width//2 - go_text.get_width()//2, 100))
        score_text = font.render(f"Your Score: {score}", True, (255,255,255))
        screen.blit(score_text, (width//2 - score_text.get_width()//2, 150))
        hs_text = font.render(f"High Score: {highscore}", True, (255,255,255))
        screen.blit(hs_text, (width//2 - hs_text.get_width()//2, 200))
        play_again = draw_button("Play Again", width//2 - 175, 300, 150, 50, (0,128,0), (0,200,0))
        exit_button = draw_button("Exit", width//2 + 25, 300, 150, 50, (128,0,0), (200,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
        if play_again:
            return 'play'
        if exit_button:
            return 'exit'
        pygame.display.flip()
        clock.tick(30)

# Main loop
while True:
    choice = menu()
    if choice == 'exit':
        break
    save_last_color(choice)
    snake_color = color_map[choice]
    result = game(snake_color)
    if result == 'quit':
        break
    choice = game_over(result)
    if choice == 'exit':
        break

pygame.quit()
sys.exit()