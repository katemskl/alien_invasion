class Settings:
    """КЛАС ДЛЯ ХРАНЕНИЯ ВСЕХ НАСТРОЕК ИГРЫ Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # Параметры корабля
        self.ship_speed_factor = 1.5

        # Параметры пули
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

