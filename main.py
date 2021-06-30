import sys
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Trouble")
icon = pygame.image.load('games.png')
pygame.display.set_icon(icon)

mixer.music.load("background.wav")
mixer.music.play(-1)

def game():

    import math
    import random

    import pygame
    from pygame import mixer

    # Player
    playerImg = pygame.image.load('spaceship.png')
    playerImg = pygame.transform.scale(playerImg, (50, 50))
    playerX = 580
    playerY = 650
    playerX_change = 0

    # Enemy
    enemyImg = pygame.image.load('alien.png')
    enemyImg = pygame.transform.scale(enemyImg, (50, 50))
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    noofenemies = 1

    # Background
    bgImg = pygame.image.load('background.jpg')
    bgx = 0
    bgy = 0

    # Bullet
    bulletImg = pygame.image.load('ammunition.png')
    bulletImg = pygame.transform.scale(bulletImg, (50, 50))
    bulletX = 0
    bulletY = 680
    bulletY_change = 3

    # Enemy bullet
    ebulletImg = pygame.image.load('bullet.png')
    ebulletImg = pygame.transform.scale(ebulletImg, (50, 50))
    ebulletX = 0
    ebulletY = 0
    ebulletY_change = 2

    bullet_state = 'ready'
    ebullet_state = "ready"

    # Scoreboard
    score = 0
    level = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    textx = 10
    texty = 10

    # Functions

    def bg(x, y):
        screen.blit(bgImg, (x, y))

    def scoreboard(x, y):
        sc = font.render("Score :  " + str(level * 100 + score), True, (255, 255, 255))
        sc2 = font.render("Level  :  " + str(level), True, (255, 255, 255))
        screen.blit(sc, (x, y))
        screen.blit(sc2, (x, y + 25))

    def new_enemy():
        for i in range(noofenemies):
            enemyX.append(random.randint(0, 1160))
            enemyY.append(random.randint(10, 100))
            enemyX_change.append((random.randint(15, 25) / 100))
            enemyY_change.append(4)

    def enemy(x, y, i):
        screen.blit(enemyImg, (x, y))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def shoot(x, y):
        global bullet_state
        bullet_state = 'fire'
        screen.blit(bulletImg, (x, y))


    def enemy_bullet(x, y):
        global ebullet_state
        ebullet_state = "fire"
        screen.blit(ebulletImg, (x, y))

    def collision(enemyx, bulletx, enemyy, bullety):
        distance = math.sqrt((math.pow((enemyx - bulletx), 2)) + (math.pow((enemyy - bullety), 2)))
        if bullet_state == "fire":
            if distance < 20:
                return True
            else:
                return False

    def ecollision(playerx, ebulletx, playery, ebullety):
        distance_e = math.sqrt((math.pow((playerx - ebulletx), 2)) + (math.pow((playery - ebullety + 40), 2)))
        if ebullet_state == "fire":
            if distance_e < 27:
                return True
            else:
                return False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                        bulletX = playerX
                        shoot(bulletX, bulletY)
                        bullet = mixer.Sound('mixkit-retro-arcade-casino-notification-211.wav')
                        bullet.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 1150:
            playerX = 1150

        bg(bgx, bgy)

        new_enemy()

        for x in range(noofenemies):
            for i in range(noofenemies):
                if enemyX[x] <= playerX or enemyX[x] >= playerX:
                    if ebullet_state == "ready":
                        ebulletX = enemyX[x]
                        ebulletY = enemyY[x] + 30
                        enemy_bullet(ebulletX, ebulletY)
                        ebullet_state = "fire"

        if ebullet_state == "fire":
            enemy_bullet(ebulletX, ebulletY)
            ebulletY += ebulletY_change

        if ebulletY >= 1360:
            ebullet_state = "ready"

        for i in range(noofenemies):
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] += 0.5
                enemyY[i] += 3

            elif enemyX[i] >= 1150:
                enemyX_change_neg = -(enemyX_change[i])
                enemyX_change_neg += -0.5
                enemyX_change[i] = enemyX_change_neg
                enemyY[i] += 20

            if collision(enemyX[i], bulletX, bulletY, enemyY[i] + 32):
                bulletY = 1160
                bullet_state = "ready"
                score += 10
                enemyX[i] = (random.randint(0, 1160))
                enemyY[i] = (random.randint(10, 50))
                enemyX_change[i] = ((random.randint(1, 50)) / 100)
                Collide = mixer.Sound('mixkit-arcade-mechanical-bling-210.wav')
                Collide.play()

            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            shoot(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 760
            bullet_state = 'ready'

        if score == 100:
            score = 0
            level += 1
            noofenemies += 1
            new = mixer.Sound('mixkit-positive-interface-beep-221.wav')
            new.play()

        player(playerX, playerY)

        font1 = pygame.font.Font('freesansbold.ttf', 70)
        text = font1.render("Game Over", True, (255, 255, 255))
        for i in range(noofenemies):
            if enemyY[i] >= 730 or ecollision(playerX, ebulletX, ebulletY, playerY + 32):
                ebullet_state = "ready"
                screen.fill('black')
                screen.blit(text, (420, 380))
                if enemyY[i] <= 2000:
                    over = mixer.Sound('mixkit-arcade-game-explosion-1699.wav')
                    over.play()
                for j in range(noofenemies):
                    enemyY[j] = 3000
                break

        scoreboard(textx, texty)

        pygame.display.update()


main_font = pygame.font.SysFont("cambria", 40)
main_font2 = pygame.font.SysFont("cambria", 150)
heading = main_font2.render("Space Trouble", True, (0, 0, 0))

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            game()

    def quit(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            pygame.quit()
            quit()
    def scores(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print("MAKE LEADERBOARD RN!!")

button_surface = pygame.image.load("button2.png")
button_surface = pygame.transform.scale(button_surface, (200, 75))
startbutton = Button(button_surface, 650, 550, "Start Game")
scoresbutton = Button(button_surface, 250, 550, "Scores")
quitbutton = Button(button_surface, 1050, 550, "Quit")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            startbutton.check(pygame.mouse.get_pos())
            quitbutton.quit(pygame.mouse.get_pos())
            scoresbutton.scores(pygame.mouse.get_pos())


    bg_img=pygame.image.load("background.jpg")
    screen.blit(bg_img, bg_img.get_rect())
    screen.blit(heading, (150, 200))
    startbutton.update()
    quitbutton.update()
    scoresbutton.update()

    pygame.display.update()

