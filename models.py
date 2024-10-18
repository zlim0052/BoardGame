# models.py

import pygame
import math

class Card:
    def __init__(self, character, number, card_type='normal', image=None):
        self.character = character
        self.number = number
        self.card_type = card_type
        self.is_flipped = False
        self.rect = None
        self.image = image

    def flip(self):
        self.is_flipped = not self.is_flipped

    def __getstate__(self):
        state = self.__dict__.copy()
        # del: removes the specified key from the dictionary
        del state['image']
        del state['rect']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = None
        self.rect = None

class Player:
    def __init__(self, name, character, color):
        self.name = name
        self.character = character
        self.position = 0
        self.laps_completed = 0
        self.color = color
        self.flipped_cards = []

    def move(self, steps, board):
        previous_position = self.position
        total_subsections = len(board.subsections)
        self.position = (self.position + steps) % total_subsections
        if self.position < previous_position:
            self.laps_completed += 1
        self.update_character(board)

    def move_backward(self, steps, board):
        previous_position = self.position
        total_subsections = len(board.subsections)
        self.position = (self.position - steps) % total_subsections
        if self.position > previous_position:
            self.laps_completed -= 1
        self.update_character(board)

    def update_character(self, board):
        subsection = board.subsections[self.position]
        self.character = subsection['character']

class Board:
    def __init__(self, center, radius, num_sections, board_char_images):
        self.center = center
        self.radius = radius
        self.num_sections = num_sections
        self.board_char_images = board_char_images
        self.create_sections()

    def create_sections(self):
        characters = ['dragon', 'salamander', 'bat', 'spider']
        total_subsections = self.num_sections * 3
        angle_step = 360 / total_subsections
        subsections = []
        for i in range(total_subsections):
            angle = math.radians(i * angle_step)
            x_sub = self.center[0] + self.radius * math.cos(angle)
            y_sub = self.center[1] + self.radius * math.sin(angle)
            character = characters[i % len(characters)]
            subsections.append({
                'character': character,
                'index': i,
                'position': (x_sub, y_sub)
            })
        self.subsections = subsections

    def __getstate__(self):
        """
        This method is called when the object is serialized with pickle.
        It should return a dictionary representing the object's state.

        The board_char_images attribute is not serializable, so it is removed from the state.

        Returns:
            dict: A dictionary containing the object's state.
        """
        # Copy the object's dictionary
        # __dict__: a dictionary containing the object's attributes
        # copy: creates a shallow copy of the object

        state = self.__dict__.copy() 

        # del: removes the specified key from the dictionary
        del state['board_char_images']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.board_char_images = None
