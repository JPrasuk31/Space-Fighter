import math
import pygame
import random
from pygame import mixer

#Git Changes

# Initialize the pygame package.
pygame.init()

# Declaring constants for screen size
SCREEN_WIDTH1 = 800
SCREEN_HEIGHT1 = 700

#Git 2 changes


# Getting background image
BACKGR1OUND = pygame.transform.smoothscale(pygame.image.load("spacebg.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Loading and adding background noise
mixer.music.load("Cipher2.mp3")
mixer.music.play(-1)

# Loading Bullet and Explosion Noise
bulletSound = mixer.Sound("laser.wav")


explosionSound2 = mixer.Sound("explosion.wav")

# Creating the scree
# n
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting the caption and appIcon
pygame.display.set_caption("SpaceFighter")
appIcon = pygame.image.load("space.png")
pygame.display.set_icon(appIcon)

# Setting Up scope
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
fontx = 10
fonty = 10


def show_score(x, y):
    '''
    Fuction is Used for displaying score on screen
    :param x: x co-ordinate of score display
    :param y: y co-ordinate of score display
    :return: None
    '''
    screen.blit(font.render("Score : " + str(score), True, (255, 255, 255)), (x, y))


def game_over():
    fontOver = pygame.font.Font('freesansbold.ttf', 50)
    screen.blit(fontOver.render("GAME OVER", True, (255, 255, 255)), (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2))


# Defining a Player class
class Player:
    def __init__(self):
        self.playerImage = pygame.transform.smoothscale(pygame.image.load("space.png"), (64, 64))
        # self.rect = self.playerImage.get_rect()
        self.playerX = (SCREEN_WIDTH / 2) - 32
        self.playerY = SCREEN_HEIGHT - 100
        self.changeX = 0

    def player_display(self):
        screen.blit(self.playerImage, (self.playerX, self.playerY))


# Initializing a player
player = Player()


# Defining a Enemy class
class Enemy:
    def __init__(self):
        self.enemyImage = pygame.transform.smoothscale(pygame.image.load("alien.png"), (64, 64))
        # self.rect = self.enemyImage.get_rect()
        self.enemyX = random.randint(0, SCREEN_WIDTH - 64)
        self.enemyY = SCREEN_HEIGHT - 600
        self.changeX = 0.4
        self.changeY = 65

    def enemy_display(self):
        screen.blit(self.enemyImage, (self.enemyX, self.enemyY))


# Initializing enemy
enemy = [None] * 10
for j in range(len(enemy)):
    enemy[j] = Enemy()


class Bullet:
    # State = { 0 : Bullet is Ready , 1 : Bullet is in motion }
    def __init__(self):
        self.bulletImage = pygame.transform.smoothscale(pygame.image.load("bullet.png"), (44, 44))
        # self.rect = self.bulletImage.get_rect()
        self.bulletX = 20
        self.bulletY = SCREEN_HEIGHT - 100 + 10
        self.changeY = -0.6
        self.state = 0

    def fire_bullet(self, Xplayer):
        if self.state == 0:
            bulletSound.play()
            self.bulletX = Xplayer + 10
        self.state = 1
        screen.blit(self.bulletImage, (self.bulletX, self.bulletY))


bullet = Bullet()


def collision(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    if distance < 30:
        return True
    return False


flag = True
# Game Loop
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(BACKGROUND, (0, 0))

    # Checking and defining different events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.changeX = 0.5
            if event.key == pygame.K_LEFT:
                player.changeX = -0.5
            if event.key == pygame.K_SPACE:
                bullet.fire_bullet(player.playerX)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.changeX = 0

    # Changing the player X co-ordinate
    player.playerX += player.changeX

    # Setting the boundaries for player
    if player.playerX >= SCREEN_WIDTH - 64:
        player.playerX = SCREEN_WIDTH - 64
    if player.playerX <= 0:
        player.playerX = 0

    # Enemy Movement and its boundaries
    for i in range(len(enemy)):
        if enemy[i].enemyY > SCREEN_HEIGHT - 100:
            for en in enemy:
                del en
            flag = False
            break

        enemy[i].enemyX += enemy[i].changeX
        if enemy[i].enemyX >= SCREEN_WIDTH - 64:
            enemy[i].enemyX = SCREEN_WIDTH - 64
            enemy[i].changeX = -enemy[i].changeX
            enemy[i].enemyY += enemy[i].changeY
        if enemy[i].enemyX <= 0:
            enemy[i].enemyX = 0
            enemy[i].changeX = -enemy[i].changeX
            enemy[i].enemyY += enemy[i].changeY

    if flag:
        # Bullet Movement
        if bullet.bulletY <= 0:
            bullet.bulletY = SCREEN_HEIGHT - 100 + 10
            bullet.state = 0
        if bullet.state == 1:
            bullet.fire_bullet(Xplayer=player.playerX)
            bullet.bulletY += bullet.changeY

        for i in range(len(enemy)):
            if collision(enemy[i].enemyX, enemy[i].enemyY, bullet.bulletX, bullet.bulletY):
                explosionSound.play()
                bullet.bulletY = SCREEN_HEIGHT - 100 + 10
                bullet.state = 0
                score += 1
                del enemy[i]
                enemy.append(Enemy())

            enemy[i].enemy_display()
        # Displaying Player
        player.player_display()
    show_score(fontx,fonty)

    if not flag:
        game_over()

    # Updating Display to show new content
    pygame.display.update()
