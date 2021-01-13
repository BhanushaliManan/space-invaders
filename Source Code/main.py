import pygame
from random import randint
from math import sqrt  # Importing Square Root
from math import pow  # Importing Power(For Squaring)

# Initialize Pygame
pygame.init()

'''
----------
Colors
----------
'''

default_black = (1, 1, 1)
blue = (25, 25, 200)
light_blue = (173, 252, 255)
black = (23, 23, 23)
white = (255, 255, 255)

'''
----------
Setup
----------
'''
# Loading Images
icon = pygame.image.load('assets/images/ufo.png')
player_img = pygame.image.load('assets/images/player.png')
enemy_img = []
background = pygame.image.load('assets/images/background.png')
bullet_img = pygame.image.load('assets/images/bullet.png')

# Background Sound
pygame.mixer.music.load('assets/sounds/background.wav')
pygame.mixer.music.play(-1)

# Player Coordinates
player_x = 370
player_y = 480
player_x_change = 0

# Enemies
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('assets/images/enemy.png'))
    enemy_x.append(randint(0, 735))
    enemy_y.append(randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
# When you can't see the Bullet, Its in Ready State
# When the Bullet is Moving, its in Fire State
bullet_state = "ready"

# Score Keeping
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Pygame Display settings
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))


# Spawn Player
def spawn_player(x, y):
    # Blit Means to Draw
    screen.blit(player_img, (x, y))


# Spawn Enemy
def spawn_enemy(x, y, img):
    # Blit Means to Draw
    screen.blit(enemy_img[img], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_colliding(x_1, y_1, x_2, y_2):
    distance = sqrt((pow(x_1 - x_2, 2)) + (pow((y_1 - y_2), 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))


# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, white)
    screen.blit(game_over, (200, 250))


# Main Loop
running = True
while running:
    # Change Background
    screen.fill(default_black)

    screen.blit(background, (0, 0))

    # Check For Any Events
    for event in pygame.event.get():
        # To Quit The Game
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Detect Key Presses(Keydowns)
        if event.type == pygame.KEYDOWN:
            # Check If The Key is Left Arrow Key or the "A" Key
            if (event.key == pygame.K_LEFT) or (event.key == ord('a')):
                player_x_change = -5

            # Check If The Key is Right Arrow Key or the "D" Key
            if (event.key == pygame.K_RIGHT) or (event.key == ord('d')):
                player_x_change = 5

            # Check If the Key Pressed is Space Key
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Playing Sound
                    bullet_sound = pygame.mixer.Sound('assets/sounds/laser.wav')
                    bullet_sound.play()

                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        # When Key is Released(Keyup)
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == ord('a')) or (
                    event.key == ord('d')):
                player_x_change = 0

    player_x += player_x_change

    # Check Boundaries
    if player_x <= 0:
        player_x = 0

    elif player_x >= 736:
        player_x = 736

    # Enemy Movement

    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]

        # Game Over
        if enemy_y[i] > 420:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        # Check Boundaries
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Collision
        colliding = is_colliding(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if colliding:
            # Playing Sound
            explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
            explosion_sound.play()

            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = randint(0, 735)
            enemy_y[i] = randint(50, 150)

        # Spawn Enemy
        spawn_enemy(enemy_x[i], enemy_y[i], i)

    # Checking If Bullet Is Off-Screen
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Spawn Player
    spawn_player(player_x, player_y)

    # Show Score
    show_score(text_x, text_y)

    # Update Display
    pygame.display.update()
