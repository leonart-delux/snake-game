import random
import pygame
from Logic.algorithms import Pathfinding

class BaseGameLogic:
    def __init__(self, obstacles, map_size, initial_pos):
        self.const_obstacles = obstacles
        self.temp_obstacles = set()     # Temporary obstacles on map (snakes)
        self.numb_rows, self.numb_cols = map_size
        self.initial_pos_row, self.initial_pos_col = initial_pos
        
        # all valid positions map, haven't include snake positions because it's dynamic
        self.valid_positions = {(row, col) for row in range(map_size[0]) for col in range(map_size[1])} - obstacles
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
        
    def get_next_snake_image_as_ostacles(self):
        """
        Return images of snake in next process move in all available directions
        May include obstacles accross boundaries, just don't care
        """
        next_snake_images = set(tuple(block) for block in self.snake_list)
        for dir_x, dir_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_head_row = self.head_row + dir_x
            next_head_col = self.head_col + dir_y
            next_snake_images.update((next_head_row, next_head_col))
        
        # Check for food
        # If next move can eat food, then tail is longer, just return the whole current snake and next heads
        if abs(self.head_row - self.food_row) + abs(self.head_col - self.food_col) == 1:
            return next_snake_images
        
        # If no food, remove tail
        return next_snake_images.remove(tuple(self.snake_list[0]))
                        
    def generate_random_food_position(self):
        # Don't spam food on snake
        valid_positions = self.valid_positions -  set(self.snake_list)
        return random.choice(list(valid_positions)) if valid_positions else None

    def update_snake_position(self):
        self.head_row += self.move_direction[0]
        self.head_col += self.move_direction[1]

        # Update new head position
        self.snake_list.append((self.head_row, self.head_col))
        # Check for length (in case no food is eaten or food is just eaten)
        if len(self.snake_list) > self.length_of_snake:
            # Del first element = tail of snake when no food is eaten, snake is moving only 
            del self.snake_list[0]
        
    def update_map(self, new_rows, new_cols, new_obstacles):
        """
        Update needed variables when new map is pushed in
        It's like create new logic, anyway ...
        """
        self.numb_rows = new_rows
        self.numb_cols = new_cols
        self.const_obstacles = new_obstacles
        self.valid_positions = {(row, col) for row in range(new_rows) for col in range(new_cols)} - new_obstacles

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


