import pygame
from Logic.gamelogic import *
from Logic.multiplaylogic import MultiplayerGameLogic
from Logic.ailogic import AIPlayerGameLogic

class Menu:
    def __init__(self, ui):
        self.ui = ui
        self.selected_mode = None
        self.selected_game_mode = None
        self.map_type = None
        self.current_screen = None
        
        # Options for each screen
        option_names = [] 
        option_functions = []
        
        # Font handle
        self.text_font_path = r'assets/fonts/PressStart2P-Regular.ttf'
        self.title_font_path = r'assets/fonts/KnightWarrior-w16n8.otf'

        self.title_font_size = 40
        self.subtitle_font_size = 25
        self.text_font_size = 15

    def remake_screen(self):
        self.ui.clear_screen()

        # Create border
        self.ui.display_image(3, 0, 0.15, r"assets/images/border_top_left.png")
        self.ui.display_image(self.ui.width - 67, 0, 0.15, r"assets/images/border_top_right.png")
        self.ui.display_image(self.ui.width - 67, self.ui.height - 89, 0.15, r"assets/images/border_bot_right.png")
        self.ui.display_image(3, self.ui.height - 89, 0.15, r"assets/images/border_bot_left.png")

        # Dont care about this
        self.ui.display_text_center("@ HCMUTE - 2024", self.ui.height - 14, self.ui.light_red, 15, self.title_font_path)

    def exit_game(self):
        pygame.quit()
        exit()
    
    def run_menu(self):
        # first screen will be start_screen
        next_screen = self.start_screen_handle
        while True:
            # take return screen as next screen
            # in order to prevent stack overflow
            next_screen = next_screen()
            if not next_screen:
                next_screen = self.start_screen_handle
    
    # ==========================
    #       Start screen
    # ==========================
    
    def start_screen_handle(self):
        self.remake_screen()
        self.current_screen = 'start_screen'
        
        # Display start_screen unchanged things 
        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, 100, self.title_font_path)        # Title display
        
        # Options for start_screen
        self.option_names = ['Play', 'Setting', 'Credit', 'Quit'] 
        self.option_functions = [self.start_game, self.show_setting, self.credit_screen_handle, self.exit_game]
        
        # Menu and event handler
        options = self.update_start_screen()
        return self.handle_events(self.update_start_screen, options)
    
    def update_start_screen(self, selected_option=0):
        # Options storage
        options = []
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10/4)

        # Options display
        for i in range(len(self.option_names)):
            color = self.ui.red if i == selected_option else self.ui.white
            options.append({
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding, first_opt_top_padding +  40 * i, color, self.text_font_size, self.text_font_path),
                'option_func': self.option_functions[i]
                })

        pygame.display.update()
        return options
    
    # ==========================
    #       Credit screen
    # ==========================
    
    def credit_screen_handle(self):
        self.remake_screen()
        self.current_screen = 'start_screen'
        # Display start_screen unchanged things 
        self.ui.display_text_center("OUR MEMBER", self.ui.height // 10, self.ui.white, self.subtitle_font_size, self.text_font_path)        # Title display
                
        # Options for start_screen
        self.option_names = ['22110031 Bien Xuan Huy', '22110032 Le Gia Huy', '22110037 Nguyen Tien Huy', '22110085 Nguyen Truong', 'Return'] 
        self.option_functions = [None, None, None, None, self.go_back]
        
        # Menu and event handler
        options = self.update_credit_screen()
        return self.handle_events(self.update_credit_screen, options)
    
    def update_credit_screen(self, selected_option=0):
        # Options storage
        options = []
        option_left_padding = self.ui.width // 6
        first_opt_top_padding = self.ui.height // 3
        image_paths = [ r'assets/images/mem_xhuy.png', r'assets/images/mem_ghuy.png', r'assets/images/mem_thuy.png', r'assets/images/mem_ntruong.png', r'assets/images/empty_border.png' ]

        # Options display
        for i in range(len(self.option_names)):
            color = self.ui.light_blue if i == selected_option else self.ui.white
            options.append({
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.text_font_size, self.text_font_path),
                'option_func': self.option_functions[i]
                })
        
        # Member images
        img_x = self.ui.width // (5/3)
        img_y = self.ui.height // 3.5
        # Fill old image (if appeared)
        self.ui.screen.fill((0, 0, 0), (img_x, img_y, 200, 300))
        self.ui.display_image(img_x, img_y, 0.7, image_paths[selected_option])   

        pygame.display.update()
        return options
    
    # ==========================
    #       Handle events
    # ==========================
    
    # Handle coming up events of specific screen
    def handle_events(self, update_screen, options, selected_option=0):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN and options[selected_option]['option_func']:
                        # if enter key is stroked ---> return called screen (its function) if there is
                        return options[selected_option]['option_func']
            
            update_screen(selected_option)

    # ==========================
    #   Return previous screen
    # ==========================
    
    def go_back(self):
        return self.start_screen_handle

    def show_setting(self):
        return

    def show_mode_selection(self):
        self.ui.clear_screen()
        title = self.title_font.render("Game mode", True, (255, 255, 255))
        single_player_button = self.button_font.render("Single", True, (255, 255, 255))
        multiplayer_button = self.button_font.render("Multiplayer (with AI)", True, (255, 255, 255))
        back_button = self.button_font.render("Return", True, (255, 255, 255))

        spacing = 20

        self.single_player_rect = self.ui.screen.blit(single_player_button, [self.ui.width / 4, self.ui.height / 2])
        self.multiplayer_rect = self.ui.screen.blit(multiplayer_button, [self.ui.width / 4, self.ui.height / 2 + single_player_button.get_height() + spacing])
        self.back_button_rect = self.ui.screen.blit(back_button, [10, 10])

        self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

        pygame.display.update()
        while True:
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
            title = self.title_font.render("Multiplay mode", True, (255, 255, 255))
            racing_button = self.button_font.render("Race", True, (255, 255, 255))
            battle_button = self.button_font.render("Battle", True, (255, 255, 255))
            back_button = self.button_font.render("Return", True, (255, 255, 255))

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
            title = self.title_font.render("Choose map", True, (255, 255, 255))
            no_obstacle_button = self.button_font.render("Map with no obstacles", True, (255, 255, 255))
            obstacle_button = self.button_font.render("Map with obstacles", True, (255, 255, 255))
            back_button = self.button_font.render("Return", True, (255, 255, 255))

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


    def start_game(self):
        if self.selected_mode == "single":
            if self.map_type == "no_obstacle":
                game_logic = AIPlayerGameLogic(self.ui, (self.ui.rows // 2, self.ui.cols // 2))
            elif self.map_type == "obstacle":
                pass
            game_logic.game_loop()
            
        elif self.selected_mode == "multiplayer":
            if self.selected_game_mode == "race" and self.map_type == "no_obstacle":
                game_logic = MultiplayerGameLogic(self.ui, self.map_type)
            elif self.selected_game_mode == "race" and self.map_type == "obstacle":
                pass
            elif self.selected_game_mode == "battle" and self.map_type == "obstacle":
                pass
            game_logic.game_loop()
