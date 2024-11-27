import random
import pygame
from Logic.algorithms import Pathfinding

class BaseGameLogic:
    def __init__(self, obstacles, map_size, initial_pos):
        self.obstacles = obstacles
        self.numb_rows, self.numb_cols = map_size
        self.initial_pos_row, self.initial_pos_col = initial_pos
        
        self.snake_speed = 20
        self.reset_game()

    def reset_game(self):
        # Set start position
        self.head_row = self.initial_pos_row
        self.head_col = self.initial_pos_col
        
        self.snake_list = [(self.head_row, self.head_col)]
        self.length_of_snake = 1
        self.score = 0
        self.game_over = False
        self.game_close = False
        
        self.food_row, self.food_col = self.generate_random_food_position()
        self.move_direction = [1, 0]
    
    def update_initial_pos(self, pos_row, pos_col):
        self.initial_pos_row = pos_row
        self.initial_pos_col = pos_col
    
    def update_obstacles(self, ostacles):
        self.obstacles = ostacles

    def get_snake_as_ostacles(self):
        return set(tuple(block) for block in self.snake_list)
                        
    def generate_random_food_position(self):
        # Create valid position list for food
        valid_positions = [
            (row_pos, col_pos)
            for row_pos in range(self.numb_rows)
            for col_pos in range(self.numb_cols)
            if (row_pos, col_pos) not in self.obstacles and (row_pos, col_pos) not in self.snake_list
        ]
        # No valid position 
        if not valid_positions:
            return None
        
        # Return a value in valid list
        return random.choice(valid_positions)

    def update_snake_position(self):
        self.head_row += self.move_direction[0]
        self.head_col += self.move_direction[1]

        # Update new head position
        self.snake_list.append((self.head_row, self.head_col))
        # Check for length (in case no food is eaten or food is just eaten)
        if len(self.snake_list) > self.length_of_snake:
            # Del first element = tail of snake when no food is eaten, snake is moving only 
            del self.snake_list[0]

    def check_boundaries(self):
        if (self.head_row < 0) or (self.head_row >= self.numb_rows) or (self.head_col < 0) or (self.head_col >= self.numb_cols):
            self.game_over = True
                
    def check_collisions(self):
        if ((self.head_row, self.head_col) in self.snake_list[:-1]) or ((self.head_row, self.head_col) in self.obstacles):
            self.game_over = True

    def check_eat_food(self):
        if self.head_row == self.food_row and self.head_col == self.food_col:
            # Update new food position and some states
            self.food_row, self.food_col = self.generate_random_food_position()
            self.length_of_snake += 1
            self.score += 1
            # Clear old path
            self.path = []

    def handle_game_close_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = False
                    self.game_close = True
                if event.key == pygame.K_c:
                    self.reset_game()

