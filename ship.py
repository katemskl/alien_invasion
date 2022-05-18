import pygame


class Ship:
    def __init__(self, ai_settings, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения корабля и получние прямоугольника
        self.image = pygame.image.load('images/ship2.bmp')
        self.image = pygame.transform.scale(self.image, (50, 87))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый корабль появляэться у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляем озицию корабля с учетом флагов."""
        # Обновляем атрибут center, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # Обновление атрибута rect на основании self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
