import random
import pygame
from Logic.algorithms import Pathfinding

class BaseGameLogic:
    def __init__(self, ui, map_type):
        self.ui = ui
        self.map_type = map_type
        self.snake_block = 10
        self.snake_speed = 2
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake_list = []
        self.length_of_snake = 1
        self.game_over = False
        self.game_close = False
        self.foodx, self.foody = self.random_food()
        self.score = 0

    def random_food(self):
        foodx = round(random.randrange(0, self.ui.width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.ui.height - self.snake_block) / 10.0) * 10.0
        return foodx, foody

    def handle_game_close_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = True
                    self.game_close = False
                if event.key == pygame.K_c:
                    self.reset_game()

    def check_boundaries(self):
        if self.x >= self.ui.width or self.x < 0 or self.y >= self.ui.height or self.y < 0:
            self.game_close = True

    def check_collisions(self):
        for block in self.snake_list[:-1]:
            if block == [self.x, self.y]:
                self.game_close = True




