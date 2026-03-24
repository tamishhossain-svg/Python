import pygame
import random

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800,600))

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
player_width = playerimg.get_width()
playerX = 370
playerY = 480
playerX_change = 0

# multiple enemies
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

#bullet
# ready state - cant see the bullet on the screen
#FIRE - The bullet is moving
bulletimg = pygame.image.load('Bullet png.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# font
font = pygame.font.Font(None, 50)

def show_game_over():
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (300, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y):
    screen.blit(enemyimg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX)**2 + (enemyY - bulletY)**2)**0.5
    return distance < 27


# Game loop
running = True
game_over = False
while running:

      # clear screen

    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # key pressed(speed control)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.25
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
               bulletX = playerX
               bulletY = playerY
               fire_bullet(bulletX, bulletY)

        # key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # player movement
    playerX += playerX_change

    # enforce boundaries
    playerX = max(0, min(playerX, 800 - playerimg.get_width()))

    # enemy move
    for i in range(num_of_enemies):

        # game over check
       if enemyY[i] > 440:
         game_over = True
      for j in range(num_of_enemies):
        enemyY[j] = 2000
      break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # collision
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

      enemy(enemyX[i], enemyY[i])

    # bullet move
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    if game_over:
        show_game_over()

    pygame.display.update()



