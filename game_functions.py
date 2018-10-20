import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x,
                              mouse_y)


def update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """更新屏幕并且切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    scoreboard.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """更新子弹的位置并删除已消失的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        # 创建一颗新子弹并加入到编组里
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行来可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break;


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.pre_score()
        check_high_score(stats, scoreboard)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        scoreboard.pre_level()

        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        scoreboard.pre_ship()

        # 清空子弹和外星人
        aliens.empty()
        bullets.empty()

        # 创建新的外星人
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """检查是否有外星人到达底部"""

    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
            break


def check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置设置
        ai_settings.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # 重置计分板
        scoreboard.pre_level()
        scoreboard.pre_high_score()
        scoreboard.pre_score()
        scoreboard.pre_ship()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.pre_high_score()