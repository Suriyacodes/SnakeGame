import pygame
import random
import os

pygame.init()

# Sound setup
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")
pygame.mixer.music.load("bgmusic.wav")
pygame.mixer.music.play(-1)  # Loop background music

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Load images
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (width, height))
snake_img = pygame.image.load("snake.png")
snake_img = pygame.transform.scale(snake_img, (20, 20))
food_img = pygame.image.load("food.png")
food_img = pygame.transform.scale(food_img, (20, 20))

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 25)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def plot_snake(snk_list):
    for x, y in snk_list:
        screen.blit(snake_img, (x, y))

def welcome():
    exit_game = False
    while not exit_game:
        screen.fill(white)
        text_screen("Welcome to Snake Game!", black, 150, 150)
        text_screen("Press SPACE to Play", black, 170, 180)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameloop()

def gameloop():
    pygame.mixer.music.play(-1)
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, width - 40)
    food_y = random.randint(20, height - 40)
    score = 0
    highscore = 0
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())

    snake_speed = 10

    while not exit_game:
        if game_over:
            pygame.mixer.music.stop()
            gameover_sound.play()
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            screen.fill(white)
            text_screen("Game Over! Press Enter to Restart", red, 100, 180)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 10
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -10
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -10
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = 10
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                eat_sound.play()
                food_x = random.randint(20, width - 40)
                food_y = random.randint(20, height - 40)
                snk_length += 5
                snake_speed += 0.5
                if score > highscore:
                    highscore = score

            screen.blit(bg, (0, 0))
            screen.blit(food_img, (food_x, food_y))
            text_screen(f"Score: {score}  Highscore: {highscore}", black, 10, 10)

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > width or snake_y < 0 or snake_y > height:
                game_over = True

            plot_snake(snk_list)
            pygame.display.update()
            clock.tick(snake_speed)

    pygame.quit()
    quit()

welcome()
