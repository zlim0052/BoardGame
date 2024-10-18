# main.py

# main_menu, configuration_menu, setup_new_game, and main functions
# are defined in this file. The main function is the entry point of the game.
"""
"""

import pygame
from settings import *
from models import Card, Player, Board
from views import *
from controllers import player_turn, print_players_status
from utils import load_card_images, create_deck, load_game, save_game, update_images, load_sounds
import sys

def main_menu(screen, sounds):
    """
    Display the main menu and return the user's choice.
    :param screen: pygame.Surface object
    :return: str
    """
    menu_running = True
    font = pygame.font.Font(None, 74)
    while menu_running:
        screen.fill(BLACK)
        # Draw title
        title_text = font.render('Fiery Dragon', True, WHITE)   # render() creates a new surface with the specified text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 100))    # get_rect() returns a new rect with the same size as the surface
        screen.blit(title_text, title_rect)

        # Draw buttons
        new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 300, 300, 50) # Rect(left, top, width, height): create a new rectangle
        load_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 400, 300, 50)

        pygame.draw.rect(screen, GRAY, new_game_button) # draw.rect(surface, color, rect): draw a rectangle
        pygame.draw.rect(screen, GRAY, load_game_button)

        small_font = pygame.font.Font(None, 48)
        new_game_text = small_font.render('Start New Game', True, WHITE)
        load_game_text = small_font.render('Load Saved Game', True, WHITE)

        screen.blit(new_game_text, new_game_button.move(20, 10)) # .move(x, y): move the rectangle by the specified amount
        screen.blit(load_game_text, load_game_button.move(5, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    sounds['button_click'].play()
                    return 'new'
                elif load_game_button.collidepoint(event.pos):
                    sounds['button_click'].play()
                    return 'load'

def configuration_menu(screen):
    menu_running = True
    font = pygame.font.Font(None, 36)
    number_of_sections = '8'  # Default value
    card_numbers_text = '1,2,3'  # Default values
    number_of_cards_text = '4'  # Default number of cards per character

    # Input boxes
    sections_input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, 200, 200, 40)
    card_numbers_input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, 260, 200, 40)
    cards_input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, 320, 200, 40)

    active_input = None

    while menu_running:
        screen.fill(BLACK)
        instructions = [
            'Game Configuration',
            'Enter the number of sections:',
            'Enter the numbers on the cards (comma-separated):',
            'Enter the number of cards per character:',
            'Press ENTER to continue'
        ]
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH / 2 - text_surface.get_width() / 2, 80 + i * 40))
        # Render current text
        sections_surface = font.render(number_of_sections, True, WHITE)
        card_numbers_surface = font.render(card_numbers_text, True, WHITE)
        cards_surface = font.render(number_of_cards_text, True, WHITE)
        # Draw input boxes
        pygame.draw.rect(screen, WHITE, sections_input_box, 2)
        pygame.draw.rect(screen, WHITE, card_numbers_input_box, 2)
        pygame.draw.rect(screen, WHITE, cards_input_box, 2)
        # Blit text
        screen.blit(sections_surface, (sections_input_box.x + 5, sections_input_box.y + 5))
        screen.blit(card_numbers_surface, (card_numbers_input_box.x + 5, card_numbers_input_box.y + 5))
        screen.blit(cards_surface, (cards_input_box.x + 5, cards_input_box.y + 5))
        pygame.display.flip() # Update the display, flip() is inb
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sections_input_box.collidepoint(event.pos):
                    active_input = 'sections'
                elif card_numbers_input_box.collidepoint(event.pos):
                    active_input = 'card_numbers'
                elif cards_input_box.collidepoint(event.pos):
                    active_input = 'cards'
                else:
                    active_input = None
            elif event.type == pygame.KEYDOWN:
                if active_input == 'sections':
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        number_of_sections = number_of_sections[:-1]
                    else:
                        number_of_sections += event.unicode
                elif active_input == 'card_numbers':
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        card_numbers_text = card_numbers_text[:-1]
                    else:
                        card_numbers_text += event.unicode
                elif active_input == 'cards':
                    if event.key == pygame.K_RETURN:
                        active_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        number_of_cards_text = number_of_cards_text[:-1]
                    else:
                        number_of_cards_text += event.unicode
                elif event.key == pygame.K_RETURN:
                    try:
                        num_sections = int(number_of_sections.strip())
                        if num_sections <= 0:
                            raise ValueError
                        card_numbers = [int(num.strip()) for num in card_numbers_text.split(',') if num.strip()]
                        if not card_numbers:
                            raise ValueError
                        num_cards_per_character = int(number_of_cards_text.strip())
                        if num_cards_per_character <= 0:
                            raise ValueError
                        menu_running = False
                    except ValueError:
                        display_message(screen, 'Invalid input. Please try again.')
                        number_of_sections = '8'
                        card_numbers_text = '1,2,3'
                        number_of_cards_text = '4'
        pygame.time.wait(100)
    return num_sections, card_numbers, num_cards_per_character


def setup_new_game(center, board_char_images, card_images, num_sections, card_numbers, num_cards_per_character):
    board = Board(center=center, radius=BOARD_RADIUS, num_sections=num_sections, board_char_images=board_char_images)
    deck = create_deck(card_images, card_numbers, num_cards_per_character)
    players = [
        Player('Alice', 'dragon', RED),
        Player('Bob', 'salamander', GREEN),
        Player('Charlie', 'bat', BLUE),
        Player('Diana', 'spider', YELLOW)
    ]
    current_player_index = 0
    return board, deck, players, current_player_index


def main():
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer module
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fiery Dragon')
    clock = pygame.time.Clock() # Create a clock object to control the frame rate of the game

    sounds = load_sounds()  # Load sounds here

    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Display main menu
    choice = main_menu(screen, sounds)

    if choice == 'load':
        game_state = load_game()
        if game_state:
            board = game_state['board']
            deck = game_state['deck']
            players = game_state['players']
            current_player_index = game_state['current_player_index']
            card_numbers = game_state.get('card_numbers', [1, 2, 3])
            num_sections = game_state.get('num_sections', 8)
            card_images, card_back_image, board_char_images = load_card_images(card_numbers)
            update_images(board, players, deck, card_images, board_char_images)
            num_cards_per_character = game_state.get('num_cards_per_character', 4)
        else:
            display_message(screen, "No saved game found. Starting new game.")
            sounds['game_start'].play()
            num_sections, card_numbers = configuration_menu(screen)
            card_images, card_back_image, board_char_images = load_card_images(card_numbers)
            board, deck, players, current_player_index = setup_new_game(center, board_char_images, card_images, num_sections, card_numbers, num_cards_per_character)
    else:
        num_sections, card_numbers, num_cards_per_character = configuration_menu(screen)
        card_images, card_back_image, board_char_images = load_card_images(card_numbers)
        board, deck, players, current_player_index = setup_new_game(center, board_char_images, card_images, num_sections, card_numbers, num_cards_per_character)

    running = True
    while running:
        player = players[current_player_index]
        has_won = player_turn(player, deck, board, screen, players, clock, card_back_image, card_numbers, num_cards_per_character, sounds)
        print_players_status(players)
        if has_won:
            sounds['game_end'].play()
            running = False
            continue
        current_player_index = (current_player_index + 1) % len(players)
    pygame.quit()

if __name__ == '__main__':
    main()
