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
while True:
    def terminate():  # уничтожитель
        pygame.quit()
        sys.exit()


    def end_screen():  # конечный экран
        intro_text = ["                                        GAME OVER", "",
                      "НАПОМИНАЮ",
                      "Управление: ПРОБЕЛ - прыжок",
                      "Не убейся об колонны",
                      "А ещё об потолок и пол",
                      f'Результат: {b}']

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


    def draw(screen):  # показ счета во время игры
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render(f"{b}", True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = 100
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


    hero_sprite = pygame.sprite.Group()


    class Bard(pygame.sprite.Sprite):  # герой
        image = load_image('12.png')
        image = pygame.transform.scale(image, (70, 70))

        def __init__(self, x, y, group):
            super().__init__(group)
            self.image = Bard.image
            self.rect = pygame.Rect(40, 40, 10, 10)
            self.rect.x = x
            self.rect.y = y

        def update(self):
            global j_height
            j_height += 0.5
            self.rect.y += j_height
            if -0 >= self.rect.y or self.rect.y >= 560:
                end_screen()


    all_sprites = pygame.sprite.Group()


    class Column(pygame.sprite.Sprite):  # колонны
        image = load_image("32.png")
        image = pygame.transform.scale(image, (100, 600))

        def __init__(self, x, y, group):
            super().__init__(group)
            self.image = Column.image
            self.rect = self.image.get_rect()
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
        a1 = pygame.time.get_ticks()  # это нужно для того чтобы вовремя показывался счет
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # и это тоже
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
        screen.fill((25, 25, 25))
        draw(screen)
        all_sprites.draw(screen)
        hero_sprite.draw(screen)
        all_sprites.update()
        hero_sprite.update()

        pygame.display.update()
