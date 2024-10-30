import random
import pygame

class GameLogic:
    def __init__(self, ui, mode):
        self.ui = ui
        self.snake_block = 10
        self.snake_speed = 15
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.mode = mode  
    def reset_game(self):
        self.x1 = self.ui.width / 2
        self.y1 = self.ui.height / 2
        self.x1_change = 0
        self.y1_change = 0
        self.snake_list = []
        self.length_of_snake = 1
        self.game_over = False
        self.game_close = False
        self.foodx = self.random_food()
        self.foody = self.random_food()

    def random_food(self):
        return round(random.randrange(0, self.ui.width - self.snake_block) / 10.0) * 10.0

    def game_loop(self):
        while not self.game_over:
            while self.game_close:
                self.ui.clear_screen()
                self.ui.display_message("You lose! Press Q-Quit or C-Play Again")
                self.ui.refresh_screen()
                self.handle_game_close_events()

            self.handle_events()
            self.update_snake_position()
            self.check_boundaries()
            self.update_screen()

            self.clock.tick(self.snake_speed)

    def handle_game_close_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = True
                    self.game_close = False
                if event.key == pygame.K_c:
                    self.reset_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x1_change = -self.snake_block
                    self.y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    self.x1_change = self.snake_block
                    self.y1_change = 0
                elif event.key == pygame.K_UP:
                    self.y1_change = -self.snake_block
                    self.x1_change = 0
                elif event.key == pygame.K_DOWN:
                    self.y1_change = self.snake_block
                    self.x1_change = 0

    def update_snake_position(self):
        self.x1 += self.x1_change
        self.y1 += self.y1_change

    def check_boundaries(self):
        # Làm cho màn hình thông nhau
        if self.x1 >= self.ui.width:
            self.x1 = 0
        elif self.x1 < 0:
            self.x1 = self.ui.width - self.snake_block
        if self.y1 >= self.ui.height:
            self.y1 = 0
        elif self.y1 < 0:
            self.y1 = self.ui.height - self.snake_block

    def update_screen(self):
        self.ui.clear_screen()
        self.ui.draw_food(self.foodx, self.foody, self.snake_block)

        snake_head = [self.x1, self.y1]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

        for x in self.snake_list[:-1]:
            if x == snake_head:
                self.game_close = True

        self.ui.draw_snake(self.snake_block, self.snake_list)
        self.ui.refresh_screen()

        # Kiểm tra ăn thức ăn
        if self.x1 == self.foodx and self.y1 == self.foody:
            self.foodx = self.random_food()
            self.foody = self.random_food()
            self.length_of_snake += 1
