import pygame
import random
import math
import os
import pickle

# Card class
class Card:
    def __init__(self, character, number, card_type='normal', image=None):
        self.character = character
        self.number = number
        self.card_type = card_type
        self.is_flipped = False
        self.rect = None  # For positioning on the screen
        self.image = image  # Assign the image here

    def flip(self):
        self.is_flipped = not self.is_flipped

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpickleable attributes
        del state['image']
        del state['rect']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Reinitialize unpickleable attributes
        self.image = None
        self.rect = None

# Player class
class Player:
    def __init__(self, name, character, color):
        self.name = name
        self.character = character  # Starting character
        self.position = 0  # Position index
        self.laps_completed = 0
        self.color = color
        self.flipped_cards = []

    def move(self, steps, board):
        previous_position = self.position
        total_subsections = len(board.subsections)
        self.position = (self.position + steps) % total_subsections
        if self.position < previous_position:
            self.laps_completed += 1
        # Update character based on the new position
        self.update_character(board)

    def move_backward(self, steps, board):
        previous_position = self.position
        total_subsections = len(board.subsections)
        self.position = (self.position - steps) % total_subsections
        if self.position > previous_position:
            self.laps_completed -= 1
        # Update character based on the new position
        self.update_character(board)

    def update_character(self, board):
        # Find the subsection the player is on
        subsection = board.subsections[self.position]
        self.character = subsection['character']

# Board class
class Board:
    def __init__(self, center, radius, num_sections, board_char_images):
        self.center = center
        self.radius = radius
        self.num_sections = num_sections
        self.board_char_images = board_char_images
        self.create_sections()

    def create_sections(self):
        characters = ['dragon', 'salamander', 'bat', 'spider']
        total_subsections = self.num_sections * 3  # Each section has 3 subsections
        angle_step = 360 / total_subsections
        subsections = []
        for i in range(total_subsections):
            angle = math.radians(i * angle_step)
            x_sub = self.center[0] + self.radius * math.cos(angle)
            y_sub = self.center[1] + self.radius * math.sin(angle)
            # Assign a character to each subsection
            character = characters[i % len(characters)]
            subsections.append({
                'character': character,
                'index': i,
                'position': (x_sub, y_sub)
            })
        self.subsections = subsections

    def draw(self, screen):
        # Draw the main board circle
        pygame.draw.circle(screen, (150, 150, 150), (int(self.center[0]), int(self.center[1])), self.radius + 30, 2)
        # Draw subsections
        for subsection in self.subsections:
            x_sub, y_sub = subsection['position']
            pygame.draw.circle(screen, (100, 100, 100), (int(x_sub), int(y_sub)), 20)
            # Display the character image
            character = subsection['character']
            image = self.board_char_images.get(character)
            if image:
                rect = image.get_rect(center=(int(x_sub), int(y_sub)))
                screen.blit(image, rect)
            else:
                # If image not available, display character initial
                font = pygame.font.Font(None, 24)
                text = font.render(character[0].upper(), True, (255, 255, 255))
                screen.blit(text, (x_sub - 10, y_sub - 10))

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpickleable attributes
        del state['board_char_images']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Reinitialize unpickleable attributes
        self.board_char_images = None

def load_card_images(card_width, card_height, card_numbers):
    card_images = {}
    board_char_images = {}
    characters = ['dragon', 'salamander', 'bat', 'spider', 'pirate']
    for character in characters:
        # Load card images
        for number in card_numbers:
            if character == 'pirate' and number > 2:
                continue  # Skip numbers greater than 2 for pirate cards
            filename = f"{character.replace(' ', '_')}_{number}.png"
            image_path = os.path.join('image', filename)
            try:
                image = pygame.image.load(image_path).convert_alpha()
                # Resize the image to match card dimensions
                image = pygame.transform.scale(image, (card_width, card_height))
                card_images[f"{character}_{number}"] = image
            except pygame.error as e:
                print(f"Unable to load image {image_path}: {e}")
        # Load board character image
        board_char_filename = f"{character.replace(' ', '_')}.png"
        image_path = os.path.join('image', board_char_filename)
        try:
            image = pygame.image.load(image_path).convert_alpha()
            # Resize the image
            image = pygame.transform.scale(image, (40, 40))
            board_char_images[character] = image
        except pygame.error as e:
            print(f"Unable to load board character image {image_path}: {e}")

    # Load card back image
    try:
        card_back_image = pygame.image.load('image/card_cover.png').convert_alpha()
        min_dimension = min(card_width, card_height)
        card_back_image = pygame.transform.scale(card_back_image, (min_dimension, min_dimension))
    except pygame.error as e:
        print(f"Unable to load card back image: {e}")
        card_back_image = create_circular_card_back(card_width, card_height)
    return card_images, card_back_image, board_char_images

def create_circular_card_back(card_width, card_height):
    min_dimension = min(card_width, card_height)
    card_back_image = pygame.Surface((min_dimension, min_dimension), pygame.SRCALPHA)
    pygame.draw.circle(card_back_image, (80, 80, 80), (min_dimension // 2, min_dimension // 2), min_dimension // 2)
    return card_back_image

def save_game(game_state, filename='saved_game.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(game_state, f)
    print("Game saved successfully.")

def load_game(filename='saved_game.pkl'):
    try:
        with open(filename, 'rb') as f:
            game_state = pickle.load(f)
        print("Game loaded successfully.")
        return game_state
    except FileNotFoundError:
        print("No saved game found.")
        return None

def create_deck(card_images, card_numbers):
    deck = []
    for char in ['dragon', 'salamander', 'bat', 'spider']:
        for num in card_numbers:
            image_key = f"{char}_{num}"
            image = card_images.get(image_key)
            card = Card(char, num, image=image)
            deck.append(card)
    # Add Pirate cards
    for num in card_numbers:
        if num <= 2:  # Pirate cards only have numbers up to 2
            for _ in range(2):
                image_key = f"pirate_{num}"
                image = card_images.get(image_key)
                card = Card('pirate', num, 'move_backward', image=image)
                deck.append(card)
    return deck

def draw_cards(screen, deck, card_back_image):
    # Arrange cards in a circle around the center
    center_x, center_y = screen.get_rect().center
    radius = board.radius - 100  # Adjusted radius
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
                pygame.draw.circle(screen, (80, 80, 80), (int(x), int(y)), card_width // 2)

def display_message(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width()/2, 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_player_info(screen, player):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Turn: {player.name} ({player.character})", True, (255, 255, 255))
    screen.blit(text, (20, 20))

def draw_players(screen, players, board):
    for p in players:
        subsection = board.subsections[p.position]
        x_sub, y_sub = subsection['position']
        # Adjust position slightly for each player to prevent overlap
        player_index = players.index(p)
        offset_angle = math.radians(player_index * 15)  # Slight angle offset
        x_offset = 5 * math.cos(offset_angle)
        y_offset = 5 * math.sin(offset_angle)
        x = x_sub + x_offset
        y = y_sub + y_offset
        pygame.draw.circle(screen, p.color, (int(x), int(y)), 10)

def player_turn(player, deck, board, screen, players, clock, card_back_image, card_numbers):
    turn_active = True
    save_button = pygame.Rect(screen.get_width() - 150, 20, 130, 40)
    small_font = pygame.font.Font(None, 36)
    while turn_active:
        # Wait for player to click on a card or the save button
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
                        # Save the game
                        game_state = {
                            'board': board,
                            'deck': deck,
                            'players': players,
                            'current_player_index': players.index(player),
                            'card_numbers': card_numbers,
                            'num_sections': board.num_sections
                        }
                        save_game(game_state)
                        display_message(screen, "Game saved.")
                    else:
                        for c in deck:
                            if c.rect.collidepoint(pos) and not c.is_flipped:
                                card = c
                                clicked = True
                                break
            # Update the display
            screen.fill((0, 0, 0))
            board.draw(screen)
            draw_players(screen, players, board)
            draw_cards(screen, deck, card_back_image)
            draw_player_info(screen, player)

            # Draw Save Game button
            pygame.draw.rect(screen, (100, 100, 100), save_button)
            save_text = small_font.render('Save Game', True, (255, 255, 255))
            screen.blit(save_text, save_button.move(10, 5))

            pygame.display.flip()
            clock.tick(30)

        # Process the flipped card
        card.flip()
        if card.character == 'pirate':
            player.move_backward(card.number, board)
            message = f"{player.name} moves backward {card.number} steps."
            turn_active = False
        elif card.character == player.character:
            player.move(card.number, board)
            message = f"{player.name} moves forward {card.number} steps."
            card.is_flipped = True  # Keep the card face up during the turn
            player.flipped_cards.append(card)
            # Allow the player to flip another card
            # Check if all cards are flipped
            if all(c.is_flipped for c in deck):
                turn_active = False
        else:
            message = "No match. Turn ends."
            card.flip()  # Flip the card back down
            turn_active = False

        # Display the message
        screen.fill((0, 0, 0))
        board.draw(screen)
        draw_players(screen, players, board)
        draw_cards(screen, deck, card_back_image)
        draw_player_info(screen, player)

        # Draw Save Game button
        pygame.draw.rect(screen, (100, 100, 100), save_button)
        save_text = small_font.render('Save Game', True, (255, 255, 255))
        screen.blit(save_text, save_button.move(10, 5))

        display_message(screen, message)
        clock.tick(30)

        # Check for win condition
        if player.laps_completed >= 1:
            message = f"{player.name} has won the game!"
            display_message(screen, message)
            pygame.time.wait(2000)
            return True

    # At the end of the turn, reset all cards to face down
    for c in deck:
        c.is_flipped = False
    player.flipped_cards.clear()

    return False

def print_players_status(players):
    print("Players' Status:")
    for player in players:
        print(f"{player.name}: Position {player.position}, Character {player.character}, Laps Completed {player.laps_completed}")

def update_images(board, players, deck, card_images, board_char_images, card_back_image):
    # Update card images
    for card in deck:
        image_key = f"{card.character}_{card.number}"
        card.image = card_images.get(image_key)
    # Restore board character images
    board.board_char_images = board_char_images

def main_menu(screen):
    menu_running = True
    font = pygame.font.Font(None, 74)
    while menu_running:
        screen.fill((0, 0, 0))
        # Draw title
        title_text = font.render('Fiery Dragon', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width()/2, 100))
        screen.blit(title_text, title_rect)

        # Draw buttons
        new_game_button = pygame.Rect(screen.get_width()/2 - 150, 300, 300, 50)
        load_game_button = pygame.Rect(screen.get_width()/2 - 150, 400, 300, 50)

        pygame.draw.rect(screen, (100, 100, 100), new_game_button)
        pygame.draw.rect(screen, (100, 100, 100), load_game_button)

        small_font = pygame.font.Font(None, 48)
        new_game_text = small_font.render('Start New Game', True, (255, 255, 255))
        load_game_text = small_font.render('Load Saved Game', True, (255, 255, 255))

        screen.blit(new_game_text, new_game_button.move(50, 5))
        screen.blit(load_game_text, load_game_button.move(40, 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    return 'new'
                elif load_game_button.collidepoint(event.pos):
                    return 'load'

def configuration_menu(screen):
    menu_running = True
    font = pygame.font.Font(None, 36)
    number_of_sections = '8'  # Default value as a string
    card_numbers_text = '1,2,3'  # Default values as a string

    # Input boxes for number of sections and card numbers
    sections_input_box = pygame.Rect(screen.get_width()/2 - 100, 200, 200, 40)
    card_numbers_input_box = pygame.Rect(screen.get_width()/2 - 100, 300, 200, 40)

    active_input = None  # Keep track of which input box is active

    while menu_running:
        screen.fill((0, 0, 0))
        # Draw instructions
        instructions = [
            'Game Configuration',
            'Enter the number of sections:',
            'Enter the numbers on the cards (comma-separated):',
            'Press ENTER to continue'
        ]
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (screen.get_width()/2 - text_surface.get_width()/2, 100 + i * 30))

        # Render the current text.
        sections_surface = font.render(number_of_sections, True, (255, 255, 255))
        card_numbers_surface = font.render(card_numbers_text, True, (255, 255, 255))

        # Draw input boxes
        pygame.draw.rect(screen, (255, 255, 255), sections_input_box, 2)
        pygame.draw.rect(screen, (255, 255, 255), card_numbers_input_box, 2)

        # Blit the text
        screen.blit(sections_surface, (sections_input_box.x + 5, sections_input_box.y + 5))
        screen.blit(card_numbers_surface, (card_numbers_input_box.x + 5, card_numbers_input_box.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the input boxes.
                if sections_input_box.collidepoint(event.pos):
                    active_input = 'sections'
                elif card_numbers_input_box.collidepoint(event.pos):
                    active_input = 'card_numbers'
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
                elif event.key == pygame.K_RETURN:
                    # Try to parse the inputs and return the configurations
                    try:
                        num_sections = int(number_of_sections.strip())
                        if num_sections <= 0:
                            raise ValueError
                        card_numbers = [int(num.strip()) for num in card_numbers_text.split(',') if num.strip()]
                        if not card_numbers:
                            raise ValueError
                        menu_running = False
                    except ValueError:
                        # Handle invalid input
                        display_message(screen, 'Invalid input. Please try again.')
                        number_of_sections = '8'
                        card_numbers_text = '1,2,3'
        pygame.time.wait(100)

    return num_sections, card_numbers

def setup_new_game(center, board_char_images, card_images, card_back_image, num_sections, card_numbers):
    global players, board, deck, current_player_index
    board_radius = 300
    board = Board(center=center, radius=board_radius, num_sections=num_sections, board_char_images=board_char_images)
    deck = create_deck(card_images, card_numbers)
    players = [
        Player('Alice', 'dragon', (255, 0, 0)),
        Player('Bob', 'salamander', (0, 255, 0)),
        Player('Charlie', 'bat', (0, 0, 255)),
        Player('Diana', 'spider', (255, 255, 0))
    ]
    current_player_index = 0
    print_players_status(players)

def main():
    global players, board, deck, current_player_index
    pygame.init()
    screen_width = 1200
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Fiery Dragon')
    clock = pygame.time.Clock()
    running = True

    center = (screen_width // 2, screen_height // 2)

    # Display main menu
    choice = main_menu(screen)

    if choice == 'load':
        # Load the game state
        game_state = load_game()
        if game_state:
            # Restore game state
            board = game_state['board']
            deck = game_state['deck']
            players = game_state['players']
            current_player_index = game_state['current_player_index']
            # Get configurations from saved game
            card_numbers = game_state.get('card_numbers', [1, 2, 3])
            num_sections = game_state.get('num_sections', 8)
            # Load images
            card_width = 80
            card_height = 80
            card_images, card_back_image, board_char_images = load_card_images(card_width, card_height, card_numbers)
            # Update images in objects
            update_images(board, players, deck, card_images, board_char_images, card_back_image)
        else:
            # No saved game found
            display_message(screen, "No saved game found. Starting new game.")
            num_sections, card_numbers = configuration_menu(screen)
            card_width = 80
            card_height = 80
            card_images, card_back_image, board_char_images = load_card_images(card_width, card_height, card_numbers)
            setup_new_game(center, board_char_images, card_images, card_back_image, num_sections, card_numbers)
    else:
        # Start new game
        num_sections, card_numbers = configuration_menu(screen)
        card_width = 80
        card_height = 80
        card_images, card_back_image, board_char_images = load_card_images(card_width, card_height, card_numbers)
        setup_new_game(center, board_char_images, card_images, card_back_image, num_sections, card_numbers)

    # Main game loop
    while running:
        player = players[current_player_index]
        has_won = player_turn(player, deck, board, screen, players, clock, card_back_image, card_numbers)
        print_players_status(players)
        if has_won:
            running = False
            continue
        current_player_index = (current_player_index + 1) % len(players)
    pygame.quit()

if __name__ == '__main__':
    main()
