import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        """绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """外星人位于边缘就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
