# utils.py

import pygame
import os
import pickle
from settings import *
from models import Card
import random
import sys

def load_card_images(card_numbers):
    card_images = {}
    board_char_images = {}
    characters = ['dragon', 'salamander', 'bat', 'spider', 'pirate']
    for character in characters:
        for number in card_numbers:
            if character == 'pirate' and number > 2:
                continue
            filename = f"{character.replace(' ', '_')}_{number}.png"
            image_path = os.path.join('images', filename)
            try:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                card_images[f"{character}_{number}"] = image
            except pygame.error as e:
                print(f"Unable to load image {image_path}: {e}")
        # Load board character image
        board_char_filename = f"{character.replace(' ', '_')}.png"
        image_path = os.path.join('images', board_char_filename)
        try:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (40, 40))
            board_char_images[character] = image
        except pygame.error as e:
            print(f"Unable to load board character image {image_path}: {e}")

    # Load card back image
    try:
        card_back_image = pygame.image.load('images/card_cover.png').convert_alpha()
        min_dimension = min(CARD_WIDTH, CARD_HEIGHT)
        card_back_image = pygame.transform.scale(card_back_image, (min_dimension, min_dimension))
    except pygame.error as e:
        print(f"Unable to load card back image: {e}")
        card_back_image = create_circular_card_back()

    return card_images, card_back_image, board_char_images

def create_circular_card_back():
    min_dimension = min(CARD_WIDTH, CARD_HEIGHT)
    card_back_image = pygame.Surface((min_dimension, min_dimension), pygame.SRCALPHA)
    pygame.draw.circle(card_back_image, DARK_GRAY, (min_dimension // 2, min_dimension // 2), min_dimension // 2)
    return card_back_image

def save_game(game_state, filename):
    with open(filename, 'wb') as f:
        pickle.dump(game_state, f)
    print(f"Game saved successfully to {filename}.")

def save_game_menu(screen, sounds):
    menu_running = True
    font = pygame.font.Font(None, 36)
    save_slots = ['Save Slot 1', 'Save Slot 2', 'Save Slot 3']
    save_buttons = []
    for i, slot in enumerate(save_slots):
        rect = pygame.Rect(SCREEN_WIDTH / 2-100, 200 + i * 60, 200, 50)
        save_buttons.append((rect, slot))
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render('Select a save slot:', True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))
        for rect, text in save_buttons:
            pygame.draw.rect(screen, GRAY, rect)
            slot_text = font.render(slot, True, WHITE)
            screen.blit(slot_text, (rect.x + 20, rect.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, slot in save_buttons:
                    if rect.collidepoint(event.pos):
                        sounds['button_click'].play()
                        return slot.replace(' ', '_') + '.pkl'
        pygame.time.wait(100)

def load_game(filename):
    try:
        with open(filename, 'rb') as f:
            game_state = pickle.load(f)
        print(f"Game loaded successfully from {filename}.")
        return game_state
    except FileNotFoundError:
        print(f"No saved game found in {filename}.")
        return None
    
def load_game_menu(screen, sounds):
    menu_running = True
    font = pygame.font.Font(None, 36)
    save_slots = ['Save Slot 1', 'Save Slot 2', 'Save Slot 3']
    load_buttons = []
    for i, slot in enumerate(save_slots):
        rect = pygame.Rect(SCREEN_WIDTH / 2 - 100, 200 + i * 60, 200, 50)
        load_buttons.append((rect, slot))
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render('Select Save Slot to Load', True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))
        for rect, slot in load_buttons:
            pygame.draw.rect(screen, GRAY, rect)
            slot_text = font.render(slot, True, WHITE)
            screen.blit(slot_text, (rect.x + 20, rect.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, slot in load_buttons:
                    if rect.collidepoint(event.pos):
                        sounds['button_click'].play()
                        return slot.replace(' ', '_') + '.pkl'
        pygame.time.wait(100)


def create_deck(card_images, card_numbers, num_cards_per_character):
    deck = []
    for char in ['dragon', 'salamander', 'bat', 'spider']:
        for num in card_numbers:
            image_key = f"{char}_{num}"
            image = card_images.get(image_key)
            for _ in range(num_cards_per_character):
                card = Card(char, num, image=image)
                deck.append(card)
    # Add Pirate cards
    for num in card_numbers:
        if num <= 2:
            image_key = f"pirate_{num}"
            image = card_images.get(image_key)
            for _ in range(num_cards_per_character // 2):  # Fewer pirate cards
                card = Card('pirate', num, 'move_backward', image=image)
                deck.append(card)
    random.shuffle(deck)
    return deck


def update_images(board, players, deck, card_images, board_char_images):
    for card in deck:
        image_key = f"{card.character}_{card.number}"
        card.image = card_images.get(image_key)
    board.board_char_images = board_char_images



def load_sounds():
    sounds = {}
    try:
        sounds['card_flip'] = pygame.mixer.Sound(os.path.join('sounds', 'flipcard.mp3'))
        sounds['player_move'] = pygame.mixer.Sound(os.path.join('sounds', 'moving.mp3'))
        sounds['game_start'] = pygame.mixer.Sound(os.path.join('sounds', 'start.mp3'))
        sounds['game_end'] = pygame.mixer.Sound(os.path.join('sounds', 'end.mp3'))
        sounds['button_click'] = pygame.mixer.Sound(os.path.join('sounds', 'click.mp3'))
    except pygame.error as e:
        print(f"Unable to load sound: {e}")
    return sounds
