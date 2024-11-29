import random
import pygame
from Logic.algorithms import Pathfinding

class BaseGameLogic:
    def __init__(self, obstacles, map_size):
        self.const_obstacles = obstacles
        self.temp_obstacles = set()     # Temporary obstacles on map (snakes)
        self.numb_rows, self.numb_cols = map_size
        
        # all valid positions map, haven't include snake positions because it's dynamic
        self.valid_positions = {(row, col) for row in range(map_size[0]) for col in range(map_size[1])} - obstacles
        self.all_directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
        self.snake_speed = 20
        self.is_initialized = False

    def initialize(self):
        # Set start position
        self.head_row, self.head_col = self.generate_random_snake_initial_position()
        
        self.snake_list = [(self.head_row, self.head_col)]
        self.length_of_snake = 1
        self.score = 0
        self.game_over = False
        
        self.food_row, self.food_col = self.generate_random_food_position()
        self.move_direction = [-1, 0]
        self.is_initialized = True
    
    def generate_random_snake_initial_position(self):
        temp_valid_positions = self.valid_positions - self.temp_obstacles
        return random.choice(list(temp_valid_positions)) if temp_valid_positions else None
                                    
    def generate_random_food_position(self):
        # Don't spam food on snake
        temp_valid_positions = self.valid_positions - self.temp_obstacles - set(self.snake_list)
        return random.choice(list(temp_valid_positions)) if temp_valid_positions else None
    
    def get_snake_as_obstacles(self):
        """
        Get snake and food as obstacles
        """
        snake_obstacles = set(tuple(block) for block in self.snake_list)
        snake_obstacles.add((self.food_row, self.food_col))
        return snake_obstacles
      
    def get_next_snake_image_as_ostacles(self):
        """
        Return images of snake in next process move in all available directions
        """
        next_snake_images = set(tuple(block) for block in self.snake_list)
        next_snake_images.add((self.food_row, self.food_col))
        
        for dir in self.all_directions:
            # May include body, but add() wont add, dont mind
            next_head = (self.head_row + dir[0]) % self.numb_rows, (self.head_col + dir[1]) % self.numb_cols
            next_snake_images.add(next_head)
            
        # Check for food
        # If length == 1 then current position acts like 1 of the next move, just return
        # If next move can eat food, then tail is longer, just return with the whole current body
        if self.length_of_snake == 1 or (min(abs(self.head_row - self.food_row), self.numb_rows - abs(self.head_row - self.food_row)) + min(abs(self.head_col - self.food_col), self.numb_cols - abs(self.head_col - self.food_col)) == 1):
            return next_snake_images
        
        # No special cases, remove tail
        next_snake_images.discard(tuple(self.snake_list[0]))
        return next_snake_images

    def remove_food_in_temp_obstacles(self):
        if (self.food_row, self.food_col) in self.temp_obstacles:
            self.temp_obstacles.remove((self.food_row, self.food_col))

    def remove_next_snake_head_in_temp_obstacles(self):
        """
        Remove NEXT snake head position in temporary obstacles list
        """
        backward_direction = (-self.move_direction[0], -self.move_direction[1])
        
        # For all but backward direction of current moving direction
        for dir in self.all_directions - {backward_direction}:
            next_head = (
                (self.head_row + dir[0]) % self.numb_rows, 
                (self.head_col + dir[1]) % self.numb_cols
                )
            self.temp_obstacles.discard(next_head)
                
        # If snake length is 1, remove backward direction too
        if self.length_of_snake == 1:
            next_head = (
                (self.head_row + backward_direction[0]) % self.numb_rows,
                (self.head_col + backward_direction[1]) % self.numb_cols
                )
            self.temp_obstacles.discard(next_head)

    def update_snake_position(self):
        self.head_row = (self.head_row + self.move_direction[0]) % self.numb_rows
        self.head_col = (self.head_col + self.move_direction[1]) % self.numb_cols
        
        self.check_eat_food()

        # Update new head position
        self.snake_list.append((self.head_row, self.head_col))
        # Check for length (in case no food is eaten or food is just eaten)
        if len(self.snake_list) > self.length_of_snake:
            # Del first element = tail of snake when no food is eaten, snake is moving only 
            del self.snake_list[0]
    
    def check_validation(self):      
        self.check_collisions()
                
    def check_collisions(self):
        # Obstacles - Other snakes - Its body
        if (self.head_row, self.head_col) in (self.temp_obstacles | self.const_obstacles) or (self.head_row, self.head_col) in self.snake_list[:-1]:
            self.game_over = True

    def check_eat_food(self):
        if self.head_row == self.food_row and self.head_col == self.food_col:
            # Update new food position and some states
            self.food_row, self.food_col = self.generate_random_food_position()
            self.length_of_snake += 1
            self.score += 1
            # Clear old path
            self.path = []


