# views.py

import pygame
# Import the settings module, * means import everything
from settings import *
import math

def draw_board(screen, board):
    pygame.draw.circle(screen, LIGHT_GRAY, (int(board.center[0]), int(board.center[1])), board.radius + 30, 2)
    for subsection in board.subsections:
        x_sub, y_sub = subsection['position']
        pygame.draw.circle(screen, GRAY, (int(x_sub), int(y_sub)), 20)
        character = subsection['character']
        image = board.board_char_images.get(character) 
        if image:
            rect = image.get_rect(center=(int(x_sub), int(y_sub)))
            screen.blit(image, rect)
        else:
            font = pygame.font.Font(None, 24)
            text = font.render(character[0].upper(), True, WHITE)
            screen.blit(text, (x_sub - 10, y_sub - 10))

def draw_players(screen, players, board):
    for p in players:
        subsection = board.subsections[p.position]
        x_sub, y_sub = subsection['position']
        player_index = players.index(p)
        offset_angle = math.radians(player_index * 15)
        x_offset = 5 * math.cos(offset_angle)
        y_offset = 5 * math.sin(offset_angle)
        x = x_sub + x_offset
        y = y_sub + y_offset
        pygame.draw.circle(screen, p.color, (int(x), int(y)), 10)

def draw_cards(screen, deck, card_back_image, board):
    center_x, center_y = screen.get_rect().center
    radius = board.radius - 100
    card_width = card_back_image.get_width()
    card_height = card_back_image.get_height()
    num_cards = len(deck)
    angle_step = 360 / num_cards
    for index, card in enumerate(deck):
        angle = math.radians(index * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        card.rect = pygame.Rect(x - card_width / 2, y - card_height / 2, card_width, card_height)
        if card.is_flipped and card.image:
            screen.blit(card.image, card.rect)
        else:
            if card_back_image:
                rect = card_back_image.get_rect(center=(int(x), int(y)))
                screen.blit(card_back_image, rect)
            else:
                pygame.draw.circle(screen, DARK_GRAY, (int(x), int(y)), card_width // 2)

def display_message(screen, message):
    """
    Display a message in the center of the screen for 2 seconds.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width()/2, 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_player_info(screen, player):
    """
    Display the current player's name and character on the screen.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(f"Turn: {player.name} ({player.character})", True, WHITE)
    screen.blit(text, (20, 20))
