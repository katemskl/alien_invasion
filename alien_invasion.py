import sys

import pygame

from settings import Settings


def run_game():
    # Инициализирует pygame, settings и объект экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # Назначение цвета фона
    bg_color = (230, 230, 230)

    # Запуск нового экрана игры
    while True:
        # Отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            # При каждом проходе цикла перерисовывается экран
            screen.fill(ai_settings.bg_color)
            if event.type == pygame.QUIT:
                sys.exit()

        # Отоброжение последнего прорисованого экрана
        pygame.display.flip()


run_game()
