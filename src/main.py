"""メインゲームループ"""
import pygame
import sys
from constants import *
from player import Player
from map import Map
from ui import DialogueBox
from battle import Battle

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
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    current_map_id = 0
    current_map = Map(current_map_id)
    dialogue_box = DialogueBox()
    battle = None
    
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
            
            # マップ遷移
            if player.y <= 0 and current_map_id == 0:  # 村から北へ
                current_map_id = 1
                current_map = Map(current_map_id)
                player.y = SCREEN_HEIGHT - player.size - 10
            elif player.y >= SCREEN_HEIGHT - player.size and current_map_id == 1:  # 森から南へ
                current_map_id = 0
                current_map = Map(current_map_id)
                player.y = 10
            
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
        
        # 描画処理
        screen.fill(BLACK)
        
        # マップ描画
        current_map.draw_tiles(screen)
        current_map.draw_obstacles(screen)
        
        # NPC描画
        for npc in current_map.npcs:
            npc.draw(screen, font)
            # インタラクションヒント
            if npc.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                hint_text = font.render("スペースキーで話す", True, YELLOW)
                hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                screen.blit(hint_text, hint_rect)
        
        # 敵描画
        for enemy in current_map.enemies:
            if enemy.hp > 0:
                enemy.draw(screen, font)
                # バトルヒント
                if enemy.get_distance_to(player) < INTERACTION_DISTANCE and not dialogue_box.active and not (battle and battle.active):
                    hint_text = font.render("スペースキーで戦う", True, YELLOW)
                    hint_rect = hint_text.get_rect(center=(player.x + player.size // 2, player.y - 20))
                    screen.blit(hint_text, hint_rect)
        
        # プレイヤー描画
        player.draw(screen)
        
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