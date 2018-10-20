class Settings():
    """存储设置"""

    def __init__(self):
        """初始化游戏设置"""

        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 7

        # 飞船设置
        self.ship_limit = 3

        # 外星人设置
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.3
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1.1
        self.alien_speed_factor = 0.9
        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
