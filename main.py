import os
import random
import sys
import sqlite3

import pygame
from pygame import *
from pygame.time import Clock

pygame.init()
j_height = -10  # высота прыжка
timer = pygame.time.Clock()
up_duration = 333
column_duration = 3000
pygame.time.set_timer(pygame.USEREVENT, column_duration)  # кулдаун выхода колонн
b = 0  # подчет результата
end = False


def terminate():  # уничтожитель
    pygame.quit()
    sys.exit()


def find_the_record():
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    c = cur.execute('''SELECT record FROM records
        WHERE id = 1''').fetchone()[0]
    return c


def change_the_record(new_record):
    con = sqlite3.connect('my.db')
    cur = con.cursor()
    cur.execute(f'''UPDATE records
            SET record = {b}
            WHERE id = 1''')
    con.commit()


def end_screen():  # конечный экран
    c = find_the_record()
    if b > c:
        change_the_record(b)
        c = b
    intro_text = ["                                        GAME OVER", "",
                  "НАПОМИНАЮ",
                  "Управление: ПРОБЕЛ - прыжок",
                  "Не убейся об колонны",
                  "А ещё об потолок и пол",
                  f'Результат: {b}',
                  f'Рекорд: {c}']

    screen.fill((55, 55, 55))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
                break
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_score(screen):  # показ счета во время игры
    font = pygame.font.Font(None, 50)
    text = font.render(f"{b}", True, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = 100
    screen.blit(text, (text_x, text_y))


def draw_record(screen):  # показ рекорда во время игры
    font = pygame.font.Font(None, 50)
    text = font.render(f"Рекорд: {find_the_record()}", True, (255, 255, 255))
    text_x = 10
    text_y = 560
    pygame.draw.rect(screen, (0, 0, 0), (0, 550, 220, 50))
    screen.blit(text, (text_x, text_y))


hero_sprite = pygame.sprite.Group()


class Bard(pygame.sprite.Sprite):  # герой
    image = load_image('12.png')
    image = pygame.transform.scale(image, (70, 70))

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Bard.image
        self.rect = pygame.Rect(0, 0, 60, 70)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global j_height
        j_height += 0.5
        self.rect.y += j_height
        if -10 >= self.rect.y or self.rect.y >= 560:
            end_screen()


all_sprites = pygame.sprite.Group()


def background(screen):
    image = load_image('bg.png')
    image = pygame.transform.scale(image, (800, 600))
    screen.blit(image, (0, 0))


class Column(pygame.sprite.Sprite):  # колонны
    image = load_image("32.png")
    image = pygame.transform.scale(image, (100, 600))

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Column.image
        self.rect = pygame.Rect(0, 0, 100, 585)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 2
        if pygame.sprite.spritecollideany(self, hero_sprite):
            end_screen()


size = width, height = 800, 600
hero = Bard(150, 150, hero_sprite)
screen = pygame.display.set_mode(size)
running = True
start_ticks = pygame.time.get_ticks()


def start_screen():  # стартовый экран
    intro_text = ["                                        ЗАСТАВКА", "",
                  "Управление: ПРОБЕЛ - прыжок",
                  "Не убейся об колонны",
                  "А ещё об потолок и пол",
                  "Это всё"]

    screen.fill((55, 55, 55))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


start_screen()

while running:  # начало игры
    timer.tick(60)  # FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                j_height = -10  # прыжок
        if event.type == pygame.USEREVENT:  # кулдаун колонн
            a = random.randrange(200, 500)  # рандом для подбора высоты
            colunm = Column(800, a, all_sprites)  # нижняя колонна
            colunm1 = Column(800, a - 800, all_sprites)  # верхняя колонна
            if pygame.time.get_ticks() > 8000:
                b += 1  # счёт
    background(screen)
    draw_score(screen)
    draw_record(screen)
    all_sprites.draw(screen)
    hero_sprite.draw(screen)

    all_sprites.update()
    hero_sprite.update()
    pygame.display.update()
