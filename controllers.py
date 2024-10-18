# controllers.py

import pygame
from settings import *
from utils import save_game
from views import *
from utils import save_game_menu  # Import save_game_menu from the correct module
from models import Player

def player_turn(player, deck, board, screen, players, clock, card_back_image, 
                card_numbers, num_cards_per_character, sounds):
    """
    Process a player's turn.
    :param player: Player object
    :param deck: list of Card objects
    :param board: Board object
    :param screen: Pygame screen object
    :param players: list of Player objects
    :param clock: Pygame clock object
    :param card_back_image: Pygame image object
    :param card_numbers: list of integers
    :param num_cards_per_character: integer
    :param sounds: dictionary of Pygame sound objects
    :return: True if the player has won the game, False otherwise
    
    The player_turn function processes a player's turn in the game. 
    It takes the player, deck, board, screen, players, clock, card_back_image, 
    card_numbers, num_cards_per_character, and sounds as arguments. 
    The function returns True if the player has won the game, and False otherwise.
    """

    turn_active = True
    save_button = pygame.Rect(screen.get_width() - 150, 20, 130, 40)
    small_font = pygame.font.Font(None, 36)
    while turn_active:
        card = None
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if save_button.collidepoint(pos):
                        sounds['button_click'].play()  # Play click sound
                        filename = save_game_menu(screen, sounds)
                        game_state = {
                            'board': board,
                            'deck': deck,
                            'players': players,
                            'current_player_index': players.index(player),
                            'card_numbers': card_numbers,
                            'num_sections': board.num_sections,
                            'num_cards_per_character': num_cards_per_character
                        }

                        save_game(game_state, filename)
                        display_message(screen, f"Game saved to {filename}.")
                    else:
                        for c in deck:
                            if c.rect.collidepoint(pos) and not c.is_flipped:
                                card = c
                                clicked = True
                                break
            # Update the display
            screen.fill(BLACK)
            draw_board(screen, board)
            draw_players(screen, players, board)
            draw_cards(screen, deck, card_back_image, board)
            draw_player_info(screen, player)

            # Draw Save Game button
            pygame.draw.rect(screen, GRAY, save_button)
            save_text = small_font.render('Save Game', True, WHITE)
            screen.blit(save_text, save_button.move(10, 5))

            pygame.display.flip()
            # clock: pygame.time.Clock object that controls the frame rate of the game
            # tick: method of the clock object that limits the frame rate to the specified value (FPS)
            # FPS: frames per second
            # The clock.tick(FPS) method will pause the game until the time for the next frame has elapsed.
            clock.tick(FPS)

        # Process the flipped card
        if card:
            card.flip()
            sounds['card_flip'].play()  # Play card flip sound
            if card.character == 'pirate':
                player.move_backward(card.number, board)
                sounds['player_move'].play()  # Play player move sound
                message = f"{player.name} moves backward {card.number} steps."
                turn_active = False
            elif card.character == player.character:
                player.move(card.number, board)
                message = f"{player.name} moves forward {card.number} steps."
                card.is_flipped = True
                player.flipped_cards.append(card)
                if all(c.is_flipped for c in deck):
                    turn_active = False
            else:
                message = "No match. Turn ends."
                card.flip()
                turn_active = False

        # Display the message
        screen.fill(BLACK)
        draw_board(screen, board)
        draw_players(screen, players, board)
        draw_cards(screen, deck, card_back_image, board)
        draw_player_info(screen, player)

        # Draw Save Game button
        pygame.draw.rect(screen, GRAY, save_button)
        save_text = small_font.render('Save Game', True, WHITE)
        screen.blit(save_text, save_button.move(10, 5))

        display_message(screen, message)
        clock.tick(FPS)

        # Check for win condition
        if player.laps_completed >= 1:
            message = f"{player.name} has won the game!"
            display_message(screen, message)
            pygame.time.wait(2000)
            return True

    # Reset cards at the end of the turn
    for c in deck:
        c.is_flipped = False
    player.flipped_cards.clear()

    return False

def print_players_status(players):
    print("Players' Status:")
    for player in players:
        print(f"{player.name}: Position {player.position}, Character {player.character}, Laps Completed {player.laps_completed}")
