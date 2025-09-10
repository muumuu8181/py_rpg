"""カメラシステムの定義"""
from constants import *

class Camera:
    def __init__(self, target):
        self.target = target  # 追従する対象（プレイヤー）
        self.x = 0
        self.y = 0
        self.smoothing = 0.1  # カメラの滑らかさ（0.1 = ゆっくり、1.0 = 即座）
        
    def update(self, map_width, map_height):
        """カメラ位置を更新"""
        # プレイヤーを画面中央に配置する位置を計算
        target_x = self.target.x - SCREEN_WIDTH // 2
        target_y = self.target.y - SCREEN_HEIGHT // 2
        
        # スムージング効果
        self.x += (target_x - self.x) * self.smoothing
        self.y += (target_y - self.y) * self.smoothing
        
        # マップの境界内に制限
        self.x = max(0, min(self.x, map_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, map_height - SCREEN_HEIGHT))
    
    def apply(self, entity_x, entity_y):
        """エンティティの描画位置を計算"""
        return (entity_x - self.x, entity_y - self.y)
    
    def apply_rect(self, rect):
        """矩形の描画位置を計算"""
        return (rect.x - self.x, rect.y - self.y, rect.width, rect.height)