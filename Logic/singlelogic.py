from Logic.gamelogic import *

class SinglePlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, map_type):
        super().__init__(ui, map_type)
        self.x = self.ui.width / 4
        self.y = self.ui.height / 4
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