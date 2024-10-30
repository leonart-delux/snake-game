import pygame
from Logic.gamelogic import GameLogic

class Menu:
    def __init__(self, ui):
        self.ui = ui
        self.selected_mode = None
        self.selected_game_mode = None
        self.map_type = None
        self.start_button_rect = None
        self.single_player_rect = None
        self.multiplayer_rect = None
        self.racing_button_rect = None
        self.battle_button_rect = None
        self.no_obstacle_rect = None
        self.obstacle_rect = None
        self.back_button_rect = None
        self.previous_state = None

    def run_menu(self):
        while True:
            self.ui.clear_screen()
            self.show_start_menu()
            pygame.display.update()
            self.handle_events()

    def show_start_menu(self):
        font = pygame.font.SysFont("arial", 70)
        title = font.render("Snake Game", True, (255, 255, 255))
        start_button = font.render("Start", True, (255, 255, 255))

        self.start_button_rect = self.ui.screen.blit(start_button, [self.ui.width / 2 - 100, self.ui.height / 2])
        self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.previous_state = 'start_menu'
                        self.show_mode_selection()
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.go_back()

    def show_mode_selection(self):
        self.previous_state = 'mode_selection'
        while True:
            self.ui.clear_screen()
            font = pygame.font.SysFont("arial", 50)
            title = font.render("Choose game mode", True, (255, 255, 255))
            single_player_button = font.render("Single", True, (255, 255, 255))
            multiplayer_button = font.render("Multiplayer (with AI)", True, (255, 255, 255))
            back_button = font.render("Return", True, (255, 255, 255))

            spacing = 20

            self.single_player_rect = self.ui.screen.blit(single_player_button, [self.ui.width / 4, self.ui.height / 2])
            self.multiplayer_rect = self.ui.screen.blit(multiplayer_button, [self.ui.width / 4, self.ui.height / 2 + single_player_button.get_height() + spacing])
            self.back_button_rect = self.ui.screen.blit(back_button, [10, 10])

            self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

            pygame.display.update()
            self.handle_mode_selection_events()

    def handle_mode_selection_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.single_player_rect.collidepoint(event.pos):
                        self.selected_mode = "single"
                        self.show_map_selection()
                    elif self.multiplayer_rect.collidepoint(event.pos):
                        self.selected_mode = "multiplayer"
                        self.show_multiplayer_mode_selection()
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.go_back()

    # 2.2
    def show_multiplayer_mode_selection(self):
        self.previous_state = 'mode_selection'
        while True:
            self.ui.clear_screen()
            font = pygame.font.SysFont("arial", 50)
            title = font.render("Choose multiplayer mode", True, (255, 255, 255))
            racing_button = font.render("Race", True, (255, 255, 255))
            battle_button = font.render("Battle", True, (255, 255, 255))
            back_button = font.render("Return", True, (255, 255, 255))

            spacing = 20

            self.racing_button_rect = self.ui.screen.blit(racing_button, [self.ui.width / 4, self.ui.height / 2])
            self.battle_button_rect = self.ui.screen.blit(battle_button, [self.ui.width / 4, self.ui.height / 2 + racing_button.get_height() + spacing])
            self.back_button_rect = self.ui.screen.blit(back_button, [10, 10])

            self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

            pygame.display.update()
            self.handle_multiplayer_selection_events()

    def handle_multiplayer_selection_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.racing_button_rect.collidepoint(event.pos):
                        self.selected_game_mode = "race"
                        self.show_map_selection()
                    elif self.battle_button_rect.collidepoint(event.pos):
                        self.selected_game_mode = "battle"
                        self.start_game()
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.go_back()

    def show_map_selection(self):
        while True:
            self.ui.clear_screen()
            font = pygame.font.SysFont("arial", 50)
            title = font.render("Choose map type", True, (255, 255, 255))
            no_obstacle_button = font.render("Map with no obstacles", True, (255, 255, 255))
            obstacle_button = font.render("Map with obstacles", True, (255, 255, 255))
            back_button = font.render("Return", True, (255, 255, 255))

            spacing = 20
            self.no_obstacle_rect = self.ui.screen.blit(no_obstacle_button, [self.ui.width / 4, self.ui.height / 2])
            self.obstacle_rect = self.ui.screen.blit(obstacle_button, [self.ui.width / 4, self.ui.height / 2 + no_obstacle_button.get_height() + spacing])
            self.back_button_rect = self.ui.screen.blit(back_button, [10, 10])

            self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

            pygame.display.update()
            if self.selected_mode == "single":
                self.previous_state = 'single_mode_selection'
                self.handle_map_selection_events()
            else:
                self.previous_state = 'multiplayer_mode_selection'
                self.handle_map_selection_events_mul()

    def handle_map_selection_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.no_obstacle_rect.collidepoint(event.pos):
                        self.map_type = "no_obstacle"
                        self.start_game()
                    elif self.obstacle_rect.collidepoint(event.pos):
                        self.map_type = "obstacle"
                        self.start_game()
                    elif self.back_button_rect.collidepoint(event.pos):
                            self.go_back()
                            
    def handle_map_selection_events_mul(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.no_obstacle_rect.collidepoint(event.pos):
                        self.map_type = "no_obstacle"
                        self.start_game()
                    elif self.obstacle_rect.collidepoint(event.pos):
                        self.map_type = "obstacle"
                        self.start_game()
                    elif self.back_button_rect.collidepoint(event.pos):
                            self.go_back()

    def go_back(self):
        if self.previous_state == 'start_menu':
            self.show_start_menu()
        elif self.previous_state == 'mode_selection':
            self.show_mode_selection()
        elif self.previous_state == 'single_mode_selection':
            self.show_mode_selection()
        elif self.previous_state == 'multiplayer_mode_selection':
            self.show_multiplayer_mode_selection()
        else:
            self.show_mode_selection()

    def start_game(self):
        if self.selected_mode == "single" and self.map_type == "no_obstacle":
            game_logic = GameLogic(self.ui, self.selected_mode)
            game_logic.game_loop()
