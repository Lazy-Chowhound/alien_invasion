class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        # 游戏刚启动时的状态
        self.game_active = False
        self.ships_left = self.ai_settings.ship_limit
        self.high_score = 0
        self.level = 1
        self.reset_stats()

    def reset_stats(self):
        """初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
