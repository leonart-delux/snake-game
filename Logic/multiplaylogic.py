from Logic.gamelogic import *
from Logic.ailogic import AIPlayerGameLogic
from Logic.singlelogic import SinglePlayerGameLogic

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
            self.check_collision_multi(self.snake1, self.snake2)

            self.snake2.handle_events()
            self.snake2.update_snake_position()
            self.check_collision_multi(self.snake2, self.snake1)

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
        if self.snake2.game_close:
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