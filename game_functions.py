import sys

from time import sleep

import pygame

from bullet import Bullet

from alien import Alien


def save_high_score(score):
    with open('high_score.txt', 'w') as file_h_s:
        file_h_s.write(str(score))


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули"""
    # Обновляет позиции пуль
    bullets.update()
    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
            if stats.score >= 20:
                stats.score -= ai_settings.missing_bullet_points
                sb.prep_score()
        # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_collision(stats, ai_settings, sb, bullets, aliens):
    """Удаление пуль и пришельцев участвующих в коллизиях и начисление за них баллов"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)


def start_new_level(screen, ai_settings, stats, sb, ship, aliens, bullets):
    """ Если весь флот уничтожен, начинается следующий уровень
         Уничтожение пуль, повышение скорости и создание нового флота"""
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # Увелечение уровня
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами"""
    check_collision(stats, ai_settings, sb, bullets, aliens)
    start_new_level(screen, ai_settings, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Реагирует на нажатие клавиш"""
    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
        score = stats.high_score
        save_high_score(score)
        sys.exit()
    elif event.key == pygame.K_p:
        stats.game_active = True
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, pushed_p=True)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максмум еще не достигнут"""
    # Создание новой пули и включение ее в групу bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score = stats.high_score
            save_high_score(score)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb,  play_button, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_mouse_position(play_button, stats, mouse_x, mouse_y):
    """Проверяет находиться ли мышь в зоне действия кнопки"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        return True


def reset_game(ai_settings, stats, sb):
    """Сброс прошлой игры"""
    # Сброс игровых настроек
    ai_settings.initialize_dynamic_settings()
    # Указатель мыши скрывается
    pygame.mouse.set_visible(False)
    # Сброс игровой статистики
    stats.reset_stats()
    stats.game_active = True

    # Сброс изображений счетов и уровня
    sb.prep_all()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x=0, mouse_y=0, pushed_p=False):
    """Запускает новую игру при нажатии кнопки Play"""
    if check_mouse_position(play_button, stats, mouse_x, mouse_y) or pushed_p:
        reset_game(ai_settings, stats, sb)

        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        start_new_game(screen, ai_settings, ship, aliens)


def start_new_game(screen, ai_settings, ship, aliens):
    """Создает обьекты для новой игры"""
    # Создание нового флота и размещение корабля в центре
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    # Создание пришельца и вычесление количества пришельцев в ряду

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размищение его в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцами"""
    if stats.ships_left > 0:
        # Уменьшение ships_left
        stats.ships_left -= 1

        sb.prep_ships()

        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        score = stats.high_score
        save_high_score(score)
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий "пришелец - корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # Проверка пришельцев, добравшихся до нижнего края экрана
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    # Все пули выводяться позади изборажений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отоброжение последнего прорисованного экрана
    pygame.display.flip()
