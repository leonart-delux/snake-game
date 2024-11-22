import random
import pygame
from Logic.algorithms import Pathfinding

class BaseGameLogic:
    def __init__(self, ui, map_type):
        self.ui = ui
        self.map_type = map_type
        self.snake_block = 10
        self.snake_speed = 30
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

class SinglePlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, map_type):
        super().__init__(ui, map_type)
        self.x = self.ui.width / 2
        self.y = self.ui.height / 2
        self.x_change = 0
        self.y_change = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.x_change != self.snake_block:
                    self.x_change = -self.snake_block
                    self.y_change = 0
                elif event.key == pygame.K_RIGHT and self.x_change != -self.snake_block:
                    self.x_change = self.snake_block
                    self.y_change = 0
                elif event.key == pygame.K_UP and self.y_change != self.snake_block:
                    self.y_change = -self.snake_block
                    self.x_change = 0
                elif event.key == pygame.K_DOWN and self.y_change != -self.snake_block:
                    self.y_change = self.snake_block
                    self.x_change = 0
                    
    def game_loop(self):
        while not self.game_over:
            while self.game_close:
                self.ui.clear_screen()
                self.ui.display_message("You lose! Press Q-Quit or C-Play Again")
                self.ui.refresh_screen()
                self.handle_game_close_events()

            self.handle_events()
            self.update_snake_position()
            self.check_collisions()
            self.check_boundaries()
            self.update_screen()

            self.clock.tick(self.snake_speed)

    def update_snake_position(self):
        self.x += self.x_change
        self.y += self.y_change

        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

        self.check_collisions() 
                
    def update_screen(self):
        self.ui.clear_screen()
        self.ui.draw_food((self.foodx, self.foody), self.ui.light_blue)
        self.ui.draw_snake(self.snake_block, self.snake_list, self.ui.blue)
        self.ui.display_text(f"Score: {self.score}", 10, 10, self.ui.blue, 20)
        self.ui.refresh_screen()

        if self.x == self.foodx and self.y == self.foody:
            self.foodx, self.foody = self.random_food()
            self.length_of_snake += 1
            self.score += 1

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, map_type):
        super().__init__(ui, map_type)
        self.x = self.ui.width * 3 / 4
        self.y = self.ui.height / 2
        self.x_change = 0
        self.y_change = 0
        self.pathfinding = Pathfinding((self.ui.width, self.ui.height), self.snake_block)
        self.path = []

    def handle_events(self):
        if not self.path:
            obstacles = set(tuple(block) for block in self.snake_list)
            start = (self.x, self.y)
            goal = (self.foodx, self.foody)
            self.path = self.pathfinding.find_path(start, goal, obstacles)
        
        if self.path:
            next_move = self.path[0]
            
            if list(next_move) in self.snake_list:
                obstacles = set(tuple(block) for block in self.snake_list)
                self.path = self.pathfinding.find_path((self.x, self.y), (self.foodx, self.foody), obstacles)
                if self.path:
                    next_move = self.path.pop(0)
                # else:
                #     self.game_close = True
            else:
                self.path.pop(0)
                self.x_change = next_move[0] - self.x
                self.y_change = next_move[1] - self.y
            
    def game_loop(self):
        while not self.game_over:
            while self.game_close:
                self.ui.clear_screen()
                self.ui.display_message("You lose! Press Q-Quit or C-Play Again")
                self.ui.refresh_screen()
                self.handle_game_close_events()

            self.handle_events()
            self.update_snake_position()
            self.check_collisions()
            self.check_boundaries()
            self.update_screen_AI()

            self.clock.tick(self.snake_speed)

    def update_snake_position(self):
        self.x += self.x_change
        self.y += self.y_change

        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)
        
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

        self.check_collisions()

    def update_screen_AI(self):
        self.ui.clear_screen()
        self.ui.draw_food((self.foodx, self.foody), self.ui.light_red)
        self.ui.draw_snake(self.snake_block, self.snake_list, self.ui.red)
        self.ui.display_text(f"AI: {self.score}", self.ui.width - 120, 10, self.ui.red, 20)
        self.ui.refresh_screen()

        if self.x == self.foodx and self.y == self.foody:
            self.foodx, self.foody = self.random_food()
            self.length_of_snake += 1
            self.score += 1
            self.path = []

class MultiplayerGameLogic:
    def __init__(self, ui, map_type):
        self.ui = ui
        self.map_type = map_type
        self.snake1 = SinglePlayerGameLogic(ui, map_type)
        self.snake2 = AIPlayerGameLogic(ui, map_type)
        self.snake1_score = 0
        self.snake2_score = 0
        self.foodx, self.foody = self.snake1.random_food()

    def game_loop(self):
        while not (self.snake1.game_close or self.snake2.game_close):
            self.snake1.handle_events()
            self.snake1.update_snake_position()
            # self.snake1.check_collisions()
            # self.snake1.check_boundaries()
            self.check_collision_multi(self.snake1, self.snake2)

            self.snake2.handle_events()
            self.snake2.update_snake_position()
            # self.snake2.check_collisions()
            # self.snake2.check_boundaries()
            self.check_collision_multi(self.snake1, self.snake2)

            self.update_multiplay_screen()
            pygame.time.Clock().tick(self.snake1.snake_speed)

        self.handle_game_close_multi()
        self.wait_for_quit()

    def update_multiplay_screen(self):
        self.ui.clear_screen()
        
        self.ui.draw_food((self.snake1.foodx, self.snake1.foody), self.ui.light_blue)  
        self.ui.draw_food((self.snake2.foodx, self.snake2.foody), self.ui.light_red)  
        self.ui.draw_snake(self.snake1.snake_block, self.snake1.snake_list, self.ui.blue)
        self.ui.draw_snake(self.snake2.snake_block, self.snake2.snake_list, self.ui.red)
        
        self.ui.display_text(f"Player: {self.snake1_score}", 10, 10, self.ui.blue, 20)
        self.ui.display_text(f"AI: {self.snake2_score}", self.ui.width - 180, 10, self.ui.red, 20)
        
        self.ui.refresh_screen()

        if self.snake1.x == self.snake1.foodx and self.snake1.y == self.snake1.foody:
            self.snake1.foodx, self.snake1.foody = self.snake1.random_food()
            self.snake1.length_of_snake += 1
            self.snake1_score += 1

        if self.snake2.x == self.snake2.foodx and self.snake2.y == self.snake2.foody:
            self.snake2.foodx, self.snake2.foody = self.snake2.random_food()
            self.snake2.length_of_snake += 1
            self.snake2_score += 1
            
    def check_collision_multi(self, player, opponent):
        if player.x >= self.ui.width or player.x < 0 or player.y >= self.ui.height or player.y < 0:
            player.game_close = True

        for block in player.snake_list[:-1]:
            if block == [player.x, player.y]:
                player.game_close = True
                
        for block in opponent.snake_list:
            if block == [player.x, player.y]:
                player.game_close = True
           
    def handle_game_close_multi(self):
        self.ui.clear_screen()
        if self.snake1.game_close:
            self.ui.display_message("Player 1 Lost! AI Wins!")
        elif self.snake2.game_close:
            self.ui.display_message("AI Lost! Player 1 Wins!")
        self.ui.refresh_screen()
        
    def wait_for_quit(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.snake1.game_over = True
                    self.snake2.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        waiting = False
                        self.snake1.game_over = True
                        self.snake2.game_over = True
