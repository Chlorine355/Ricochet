from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFont
import random
import pygame
import sys
import os
from time import sleep


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 40)  # на сайте пайгейм написано сделать так и это работает
# global varibles
score1 = 0
score2 = 0
running = True
mode = 1
size = width, height = 800, 528


# load image function
def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# starting window
class Start(QWidget):
    global mode, running

    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setGeometry(300, 40, 800, 528)
        self.setWindowTitle('Ricochet')

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap('data/поле.png'))

        self.play1 = QPushButton(self)
        self.play2 = QPushButton(self)
        self.stats = QPushButton(self)
        self.quit = QPushButton(self)

        self.play1.resize(70, 20)
        self.play1.move(367, 260)
        self.play1.setText('1 player')
        self.play2.resize(70, 20)
        self.play2.move(367, 290)
        self.play2.setText('2 players')
        self.stats.resize(70, 20)
        self.stats.move(367, 320)
        self.stats.setText('Stats')
        self.quit.resize(70, 20)
        self.quit.move(367, 350)
        self.quit.setText('Quit')
        self.title = QLabel(self)
        self.title.move(290, 130)
        self.title.setText('Ricochet')
        self.title.setFont(QFont('Calibri', 50))

        self.play1.clicked.connect(self.oneplayer)
        self.play2.clicked.connect(self.twoplayers)
        self.stats.clicked.connect(self.openstats)
        self.quit.clicked.connect(self.leave)

    def leave(self):
        sys.exit(app.exec())

    def oneplayer(self):
        global mode, running, score2, score1
        mode = 1
        running = True
        score1, score2 = 0, 0
        game()

    def twoplayers(self):
        global mode, running, score2, score1
        running = True
        mode = 2
        score1, score2 = 0, 0
        game()

    def openstats(self):
        self.st = Stats()
        self.st.show()


# stats window class
class Stats(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stats')
        self.setGeometry(500, 350, 200, 50)

        self.reset = QPushButton(self)
        self.reset.move(100, 10)
        self.reset.setText('Reset stats')
        self.reset.resize(75, 20)
        self.reset.clicked.connect(self.resets)
        self.total = QLabel(self)
        self.won = QLabel(self)
        self.total.setText('Total games: ')
        self.won.move(10, 20)
        self.total.move(10, 5)
        self.won.setText('Games won: ')
        with open('data/stats.txt', mode='r', encoding='utf-8') as f:
            d = f.readlines()
            self.won.setText('Games won: ' + d[1])
            self.total.setText('Total games: ' + d[0])

    def resets(self):
        with open('data/stats.txt', mode='w', encoding='utf-8') as f:
            f.write('0')
            f.write('\n')
            f.write('0')
        with open('data/stats.txt', mode='r', encoding='utf-8') as f:
            d = f.readlines()
            self.won.setText('Games won: ' + d[1])
            self.total.setText('Total games: ' + d[0])


# sprite groups
platforms = pygame.sprite.Group()
borders = pygame.sprite.Group()
ballgroup = pygame.sprite.Group()
goals = pygame.sprite.Group()


# classes for left and right platform
class LeftPlatform(pygame.sprite.Sprite):
    pygame.init()
    screen = pygame.display.set_mode(size)
    image = load_image("left.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = LeftPlatform.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 220


class RightPlatform(pygame.sprite.Sprite):
    screen = pygame.display.set_mode(size)
    image = load_image("right.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = RightPlatform.image
        self.rect = self.image.get_rect()
        self.rect.x = 766
        self.rect.y = 220


# ball class
class Ball(pygame.sprite.Sprite):
    screen = pygame.display.set_mode(size)
    image = load_image("шар.png")
    pygame.quit()

    def __init__(self, group):
        super().__init__(group)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = 390
        self.rect.y = 250
        self.vx = random.choice([-8, 8])
        self.vy = random.choice([-8, 8])

    def update(self):
        global score1, score2
        self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, platforms):
            self.vx = -self.vx


# game function
def game():
    global running, mode, score1, score2, pygame, size, platforms
    if mode == 1:  # 1 player
        pygame.init()
        screen = pygame.display.set_mode(size)
        for i in platforms:
            i.kill()
        for i in ballgroup:
            i.kill()
        l = LeftPlatform(platforms)
        r = RightPlatform(platforms)
        b = Ball(ballgroup)
        clock = pygame.time.Clock()
        fps = 100
        # sounds
        pygame.mixer.music.load('data/fon.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        screen_rect = (0, 0, width, height)
        sound = pygame.mixer.Sound('data/sound.wav')
        while running and score1 < 5 and score2 < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if b.rect.y >= 508 or b.rect.y <= 0:
                b.vy *= -1
                sound.play()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and r.rect.y < 409:
                r.rect.y += 7
            if keys[pygame.K_UP] and r.rect.y > 1:
                r.rect.y -= 7
            # bot strategy
            if not b.rect.y - 5 < (l.rect.y + 60) < b.rect.y + 5:
                if l.rect.y > b.rect.y + 5 and l.rect.y > 1:
                    l.rect.y -= 7
                elif l.rect.y < 409:
                    l.rect.y += 7
            b.update()
            if b.rect.x < 1:
                score2 += 1
                b.rect.x = 390
                b.rect.y = 250
                b.vx = random.choice([-8, 8])
                b.vy = random.choice([-8, 8])
                l.rect.y = 220
                r.rect.y = 220
                screen.fill((0, 0, 0))
                platforms.draw(screen)
                ballgroup.draw(screen)
                for i in range(score1):
                    pygame.draw.circle(screen, (0, 255, 0), (i * 15 + 40, 20), 4)
                for i in range(score2):
                    pygame.draw.circle(screen, (255, 0, 0), (i * 15 + 600, 20), 4)
                pygame.display.flip()
                sleep(2)
            if b.rect.x > 780:
                score1 += 1
                b.rect.x = 390
                b.rect.y = 250
                l.rect.y = 220
                r.rect.y = 220
                b.vx = random.choice([-8, 8])
                b.vy = random.choice([-8, 8])
                screen.fill((0, 0, 0))
                platforms.draw(screen)
                ballgroup.draw(screen)
                sleep(2)
            screen.fill((0, 0, 0))
            platforms.draw(screen)
            ballgroup.draw(screen)
            for i in range(score1):
                pygame.draw.circle(screen, (0, 255, 0), (i * 15 + 40, 20), 4)
            for i in range(score2):
                pygame.draw.circle(screen, (255, 0, 0), (i * 15 + 600, 20), 4)
            pygame.display.flip()
            clock.tick(fps)
        screen.fill((0, 0, 0))
        pygame.quit()
        with open('data/stats.txt', mode='r', encoding='utf-8') as f:
            d = f.readlines()
        with open('data/stats.txt', mode='w', encoding='utf-8') as f2:
            if score1 == 5:
                f2.write(str(int(d[0]) + 1))
                f2.write('\n')
                f2.write(d[1])
            elif score2 == 5:
                f2.write(str(int(d[0]) + 1))
                f2.write('\n')
                f2.write(str(int(d[1]) + 1))
            else:
                f2.write(d[0])
                f2.write(d[1])

    else:  # 2 players
        pygame.init()
        screen = pygame.display.set_mode(size)
        for i in platforms:
            i.kill()
        for i in ballgroup:
            i.kill()
        l = LeftPlatform(platforms)
        r = RightPlatform(platforms)
        b = Ball(ballgroup)
        clock = pygame.time.Clock()
        fps = 100
        # sounds
        pygame.mixer.music.load('data/fon.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        sound = pygame.mixer.Sound('data/sound.wav')
        while running and score1 < 5 and score2 < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if b.rect.y >= 508 or b.rect.y <= 0:
                b.vy *= -1
                sound.play()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and r.rect.y < 409:
                r.rect.y += 7
            if keys[pygame.K_UP] and r.rect.y > 1:
                r.rect.y -= 7
            if keys[pygame.K_s] and l.rect.y < 409:
                l.rect.y += 7
            if keys[pygame.K_w] and l.rect.y > 1:
                l.rect.y -= 7
            if b.rect.x < 1:
                score2 += 1
                b.rect.x = 390
                b.rect.y = 250
                b.vx = random.choice([-8, 8])
                b.vy = random.choice([-8, 8])
                l.rect.y = 220
                r.rect.y = 220
                screen.fill((0, 0, 0))
                platforms.draw(screen)
                ballgroup.draw(screen)
                for i in range(score1):
                    pygame.draw.circle(screen, (0, 255, 0), (i * 15 + 40, 20), 4)
                for i in range(score2):
                    pygame.draw.circle(screen, (255, 0, 0), (i * 15 + 600, 20), 4)
                pygame.display.flip()
                sleep(2)
            if b.rect.x > 780:
                score1 += 1
                b.rect.x = 390
                b.rect.y = 250
                l.rect.y = 220
                r.rect.y = 220
                b.vx = random.choice([-8, 8])
                b.vy = random.choice([-8, 8])
                screen.fill((0, 0, 0))
                platforms.draw(screen)
                ballgroup.draw(screen)
                sleep(2)
            b.update()
            screen.fill((0, 0, 0))
            for i in range(score1):
                pygame.draw.circle(screen, (0, 255, 0), (i * 15 + 40, 20), 4)
            for i in range(score2):
                pygame.draw.circle(screen, (255, 0, 0), (i * 15 + 600, 20), 4)
            platforms.draw(screen)
            ballgroup.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        screen.fill((0, 0, 0))
        pygame.quit()


# финишная прямая
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start()
    ex.show()
    sys.exit(app.exec())
