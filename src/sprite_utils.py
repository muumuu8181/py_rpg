"""スプライトシート処理ユーティリティ"""
import pygame

def load_sprite_sheet(filepath, frame_width, frame_height, scale=1.0):
    """
    スプライトシートを読み込んで個別のフレームに分割
    
    Args:
        filepath: スプライトシートのパス
        frame_width: 1フレームの幅
        frame_height: 1フレームの高さ
        scale: 拡大率（デフォルト1.0）
    
    Returns:
        フレームのリスト [[row0_frames], [row1_frames], ...]
    """
    try:
        sheet = pygame.image.load(filepath)
        sheet_width, sheet_height = sheet.get_size()
        
        frames = []
        rows = sheet_height // frame_height
        cols = sheet_width // frame_width
        
        for row in range(rows):
            row_frames = []
            for col in range(cols):
                # 各フレームを切り出す
                frame_rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
                frame = sheet.subsurface(frame_rect).copy()
                
                # スケーリング
                if scale != 1.0:
                    new_width = int(frame_width * scale)
                    new_height = int(frame_height * scale)
                    frame = pygame.transform.scale(frame, (new_width, new_height))
                
                row_frames.append(frame)
            frames.append(row_frames)
        
        return frames
    except Exception as e:
        print(f"スプライトシート読み込みエラー: {filepath}")
        print(f"エラー詳細: {e}")
        return None

def get_animation_frames(sprite_sheet, direction="down"):
    """
    方向別のアニメーションフレームを取得
    
    通常のRPGスプライトシートの配置:
    - 0行目: 下向き
    - 1行目: 左向き
    - 2行目: 右向き
    - 3行目: 上向き
    """
    if not sprite_sheet:
        return []
    
    direction_map = {
        "down": 0,
        "left": 1,
        "right": 2,
        "up": 3
    }
    
    row = direction_map.get(direction, 0)
    if row < len(sprite_sheet):
        return sprite_sheet[row]
    return []