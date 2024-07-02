import pygame #pip install pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 640, 480

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
random_color = (112, 114, 56)
blue = (0, 0, 255)

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_dir = (1, 0)
change_dir = snake_dir
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
score = 0
high_score_file = "high_score.txt"

def load_high_score():
    try:
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

high_score = load_high_score()
snake_speed = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
pygame.mixer.music.load("your_music_file.WAV")
pygame.mixer.music.play(-1, 0.0)
music_on = True

music_turn_off_button = pygame.image.load("mute_button.png")
music_turn_off_button = pygame.transform.scale(music_turn_off_button, (30, 30))
music_turn_off_rect = music_turn_off_button.get_rect()
music_turn_off_rect.topleft = (WIDTH - music_turn_off_rect.width - 10, 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                snake_pos = [100, 50]
                snake_body = [[100, 50], [90, 50], [80, 50]]
                snake_dir = (1, 0)
                change_dir = snake_dir
                food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
                score = 0
                snake_speed = 15
            elif event.key == pygame.K_m:
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if music_turn_off_rect.collidepoint(event.pos):
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True

    snake_pos[0] += snake_dir[0] * 10
    snake_pos[1] += snake_dir[1] * 10
    snake_body.insert(0, list(snake_pos))

    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        snake_pos = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50]]
        snake_dir = (1, 0)
        change_dir = snake_dir
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
        score = 0
        snake_speed = 15

    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    else:
        snake_body.pop()

    for segment in snake_body[1:]:
        if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            snake_pos = [100, 50]
            snake_body = [[100, 50], [90, 50], [80, 50]]
            snake_dir = (1, 0)
            change_dir = snake_dir
            food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
            score = 0

    screen.fill(random_color)

    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, black)
    high_score_text = font.render(f'High Score: {high_score}', True, blue)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    screen.blit(music_turn_off_button, music_turn_off_rect)

    pygame.display.flip()

    pygame.time.Clock().tick(snake_speed)

    snake_dir = change_dir
    keys = pygame.key.get_pressed()
    for key in keys:
        if keys[pygame.K_LEFT] and not snake_dir == (1, 0):
            change_dir = (-1, 0)
        elif keys[pygame.K_RIGHT] and not snake_dir == (-1, 0):
            change_dir = (1, 0)
        elif keys[pygame.K_UP] and not snake_dir == (0, 1):
            change_dir = (0, -1)
        elif keys[pygame.K_DOWN] and not snake_dir == (0, -1):
            change_dir = (0, 1)