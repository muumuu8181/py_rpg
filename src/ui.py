"""UI要素の定義"""
import pygame
from constants import *

class DialogueBox:
    def __init__(self):
        self.active = False
        self.text = ""
        self.speaker = ""
        self.portrait = None
        
    def show(self, speaker, text, portrait=None):
        self.active = True
        self.speaker = speaker
        self.text = text
        self.portrait = portrait
    
    def hide(self):
        self.active = False
        self.portrait = None
    
    def draw(self, screen, font):
        if not self.active:
            return
            
        # Draw dialogue box
        box_height = 160
        box_y = SCREEN_HEIGHT - box_height - 20
        pygame.draw.rect(screen, BLACK, (20, box_y, SCREEN_WIDTH - 40, box_height))
        pygame.draw.rect(screen, WHITE, (20, box_y, SCREEN_WIDTH - 40, box_height), 2)
        
        # Draw portrait if available
        text_x_offset = 30
        if self.portrait:
            # ポートレート背景
            portrait_bg_x = 30
            portrait_bg_y = box_y + 5
            pygame.draw.rect(screen, WHITE, (portrait_bg_x - 2, portrait_bg_y - 2, 154, 154), 2)
            # ポートレート画像
            screen.blit(self.portrait, (portrait_bg_x, portrait_bg_y))
            text_x_offset = 200  # テキストを右にずらす
        
        # Draw speaker name
        speaker_text = font.render(self.speaker + ":", True, YELLOW)
        screen.blit(speaker_text, (text_x_offset, box_y + 10))
        
        # Draw dialogue text
        dialogue_text = font.render(self.text, True, WHITE)
        screen.blit(dialogue_text, (text_x_offset, box_y + 40))
        
        # Draw instruction
        instruction_text = font.render("スペースキーで閉じる", True, WHITE)
        screen.blit(instruction_text, (text_x_offset, box_y + 120))