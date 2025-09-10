"""メインゲームループ"""
import pygame
import sys
from constants import *
from player import Player
from map import Map
from ui import DialogueBox
from battle import Battle
from camera import Camera

def main():
    # Pygame初期化
    pygame.init()
    
    # フォント設定
    try:
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
    except:
        font = pygame.font.Font(None, 24)
    
    # 画面設定
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Adventure")
    clock = pygame.time.Clock()
    
    # ゲームオブジェクト作成
    player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
    current_map_id = 0
    current_map = Map(current_map_id)
    dialogue_box = DialogueBox()
    battle = None
    camera = Camera(player)
    
    # ゲームループ
    running = True
    space_pressed = False
    
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE and battle and battle.active:
                    battle.active = False
                    battle.message = "逃げ出した！"
                    battle.message_timer = 60
        
        # キー状態取得
        keys = pygame.key.get_pressed()
        
        # 更新処理
        if battle and battle.active:
            # バトルモード
            battle.update()
            if space_pressed and battle.turn == "player" and battle.message_timer == 0:
                battle.player_attack()
        elif not dialogue_box.active:
            # 通常モード
            player.move(keys, current_map.obstacles)
            
            # プレイヤーの移動速度をマップに応じて設定
            player.set_speed_for_map(current_map_id)
            
            # マップ遷移
            if player.y <= 0 and current_map_id == 0:  # 村から北へ
                current_map_id = 1
                current_map = Map(current_map_id)
                player.y = MAP_HEIGHT - player.size - 10
                player.set_speed_for_map(current_map_id)
            elif player.y >= MAP_HEIGHT - player.size and current_map_id == 1:  # 森から南へ
                current_map_id = 0
                current_map = Map(current_map_id)
                player.y = 10
                player.set_speed_for_map(current_map_id)
            
            # NPC との対話チェック
            if space_pressed:
                for npc in current_map.npcs:
                    if npc.get_distance_to(player) < INTERACTION_DISTANCE:
                        dialogue_box.show(npc.name, npc.dialogue, npc.portrait)
                        break
                
                # 敵との戦闘チェック
                for enemy in current_map.enemies:
                    if enemy.hp > 0 and enemy.get_distance_to(player) < INTERACTION_DISTANCE:
                        battle = Battle(player, enemy)
                        battle.start()
                        break
        else:
            # ダイアログモード
            if space_pressed:
                dialogue_box.hide()
        
        space_pressed = False
        
        # カメラ更新
        camera.update(MAP_WIDTH, MAP_HEIGHT)
        
        # 描画処理
        screen.fill(BLACK)
        
        # マップ描画（カメラオフセット適用）
        current_map.draw_tiles(screen, camera)
        current_map.draw_obstacles(screen, camera)
        
        # NPC描画（カメラオフセット適用）
        for npc in current_map.npcs:
            npc_x, npc_y = camera.apply(npc.x, npc.y)
            npc.draw_at_position(screen, font, npc_x, npc_y)
            # インタラクションヒント
            if npc.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                hint_text = font.render("スペースキーで話す", True, YELLOW)
                player_screen_x, player_screen_y = camera.apply(player.x, player.y)
                hint_rect = hint_text.get_rect(center=(player_screen_x + player.size // 2, player_screen_y - 20))
                screen.blit(hint_text, hint_rect)
        
        # 敵描画（カメラオフセット適用）
        for enemy in current_map.enemies:
            if enemy.hp > 0:
                enemy_x, enemy_y = camera.apply(enemy.x, enemy.y)
                enemy.draw_at_position(screen, font, enemy_x, enemy_y)
                # バトルヒント
                if enemy.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                    hint_text = font.render("スペースキーで戦う", True, YELLOW)
                    player_screen_x, player_screen_y = camera.apply(player.x, player.y)
                    hint_rect = hint_text.get_rect(center=(player_screen_x + player.size // 2, player_screen_y - 20))
                    screen.blit(hint_text, hint_rect)
        
        # プレイヤー描画（カメラオフセット適用）
        player_screen_x, player_screen_y = camera.apply(player.x, player.y)
        player.draw_at_position(screen, player_screen_x, player_screen_y)
        
        # UI描画
        dialogue_box.draw(screen, font)
        if battle:
            battle.draw(screen, font)
        
        # マップ名表示
        map_names = ["村", "森"]
        map_text = font.render(f"現在地: {map_names[current_map_id]}", True, WHITE)
        screen.blit(map_text, (10, 10))
        
        # 画面更新
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()