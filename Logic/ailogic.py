from Logic.gamelogic import *
from Logic.algorithms import Pathfinding

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, map_type):
        super().__init__(ui, map_type)
        self.x = self.ui.width * 3 / 4
        self.y = self.ui.height * 3 / 4
        self.x_change = 0
        self.y_change = 0
        self.pathfinding = Pathfinding((self.ui.width, self.ui.height), self.snake_block)
        self.path = []

    def handle_events(self):
        if not self.path:
            obstacles = set(tuple(block) for block in self.snake_list)
            start = (self.x, self.y)
            goal = (self.foodx, self.foody)
            # self.path = self.pathfinding.find_path(start, goal, obstacles)
            self.path = self.pathfinding.find_path(start, goal, obstacles)[1:]
        
        if self.path:
            # next_move = self.path[0]
            
            # if list(next_move) in self.snake_list:
            #     obstacles = set(tuple(block) for block in self.snake_list)
            #     self.path = self.pathfinding.find_path((self.x, self.y), (self.foodx, self.foody), obstacles)
            #     if self.path:
            #         next_move = self.path.pop(0)
            # else:
                # self.path.pop(0)z
            next_move = self.path.pop(0)
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

    def update_screen_AI(self):
        self.ui.clear_screen()
        self.ui.draw_food((self.foodx, self.foody), self.ui.light_red)
        self.ui.draw_snake(self.snake_list, self.ui.red)
        self.ui.display_text(f"AI: {self.score}", self.ui.width - 120, 10, self.ui.red, 20)
        self.ui.refresh_screen()

        if self.x == self.foodx and self.y == self.foody:
            self.foodx, self.foody = self.random_food()
            self.length_of_snake += 1
            self.score += 1
            self.path = []
            