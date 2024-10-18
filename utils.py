# utils.py

import pygame
import os
import pickle
from settings import *
from models import Card
import random

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

def create_deck(card_images, card_numbers, num_cards_per_character):
    deck = []
    for char in ['dragon', 'salamander', 'bat', 'spider']:
        for num in card_numbers:
            image_key = f"{char}_{num}"
            image = card_images.get(image_key)
            # for _ in range(num_cards_per_character) means that the loop will run num_cards_per_character times
            # the underscore _ is a common convention in Python to indicate that the variable is not used
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
