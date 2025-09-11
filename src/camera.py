"""カメラシステムの定義"""
from constants import *

class Camera:
    def __init__(self, target):
        self.target = target  # 追従する対象（プレイヤー）
        self.x = 0.0  # float型で精密な位置計算
        self.y = 0.0
        self.smoothing = 0.25  # カメラの滑らかさをさらに上げる
        self.deadzone = 50  # デッドゾーン（この範囲内ならカメラが動かない）
        
    def update(self, map_width, map_height):
        """カメラ位置を更新"""
        # プレイヤーを画面中央に配置する位置を計算
        target_x = self.target.x - SCREEN_WIDTH // 2
        target_y = self.target.y - SCREEN_HEIGHT // 2
        
        # 現在位置との差分
        diff_x = target_x - self.x
        diff_y = target_y - self.y
        
        # デッドゾーン内なら小さな動きはしない
        if abs(diff_x) > self.deadzone:
            self.x += diff_x * self.smoothing
        if abs(diff_y) > self.deadzone:
            self.y += diff_y * self.smoothing
        
        # マップの境界内に制限
        self.x = max(0, min(self.x, map_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, map_height - SCREEN_HEIGHT))
    
    def apply(self, entity_x, entity_y):
        """エンティティの描画位置を計算"""
        return (int(entity_x - self.x), int(entity_y - self.y))
    
    def apply_rect(self, rect):
        """矩形の描画位置を計算"""
        return (int(rect.x - self.x), int(rect.y - self.y), rect.width, rect.height)