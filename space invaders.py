import pygame
import random

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# fps clock
clock = pygame.time.Clock()
FPS = 60

# Background
background = pygame.image.load('space.png')

# music
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player64by64.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = pygame.image.load('alien type 1.jpg')
num_of_enemies = 5

enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
bulletimg = pygame.image.load('Bullet png.png')
bulletX = 0
bulletY = 480
bulletY_change = 15
bullet_state = "ready"

# Power-Up (rapid fire)
powerup_img = pygame.image.load('powerup 32.png')
powerupX = 0
powerupY = 0
powerup_active = False
powerupY_change = 3

rapid_fire = True
rapid_fire_time = 0


# Font
font = pygame.font.Font(None, 64)

# Functions
def show_game_over():
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (250, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y):
    screen.blit(enemyimg, (x, y))

def draw_powerup(x, y):
    screen.blit(powerup_img, (x, y))

def powerup_collision(px, py, x, y):
    return ((px - x) ** 2 + (py - y) ** 2) ** 0.5 < 30

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    return distance < 27

# Game loop
running = True
game_over = False

while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if rapid_fire or bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    bullet_state = "fire"

        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    playerX = max(0, min(playerX, 800 - playerimg.get_width()))

    # Enemy movement
    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            game_over = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2.5
            enemyY[i] += enemyY_change[i]

        # Collision
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

            # Spawn rapid fire power-up (
            if random.randint(0, 4) == 0:
                powerupX = enemyX[i]
                powerupY = enemyY[i]
                powerup_active = True

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

       


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Powerup movement
    if powerup_active:
        draw_powerup(powerupX, powerupY)
        powerupY += powerupY_change

        # Collect power-up
        if powerup_collision(playerX, playerY, powerupX, powerupY):
            powerup_active = False
            rapid_fire = True
            rapid_fire_time = pygame.time.get_ticks()

    # Rapid fire time
    if rapid_fire:
        if pygame.time.get_ticks() - rapid_fire_time > 5000:
            rapid_fire = False


    # Draw player
    player(playerX, playerY)

    # Game over text
    if game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(60)
