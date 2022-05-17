import pygame


class Ship:
    def __init__(self, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = screen

        # Загрузка изображения корабля и получние прямоугольника
        self.image = pygame.image.load('images/ship2.bmp')
        self.image = pygame.transform.scale(self.image, (50, 87))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый корабль появляэться у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Флаш перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляем озицию корабля с учетом флага."""
        if self.moving_right:
            self.rect.centerx += 1
        if self.moving_left:
            self.rect.centerx -= 1

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
