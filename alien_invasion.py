import pygame
from settings import Settings
from ship import Ship
import game_functions
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    game_functions.create_fleet(ai_settings, screen, ship, aliens)

    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, "Play")

    while True:
        game_functions.check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            game_functions.update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
            game_functions.update_aliens(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
        # 重绘屏幕
        game_functions.update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button)


run_game()
