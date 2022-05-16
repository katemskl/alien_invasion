import sys

import pygame


def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Alien Invasion')

    # Запуск нового экрана игры
    while True:
        # Отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Отоброжение последнего прорисованого экрана
        pygame.display.flip()


run_game()
