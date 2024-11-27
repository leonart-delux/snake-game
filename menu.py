import pygame
from Logic.gamelogic import *
from Logic.multiplaylogic import MultiplayerGameLogic
from Logic.ailogic import AIPlayerGameLogic
from obstacles import ObstacleMap

class Menu:
    def __init__(self, ui):
        self.ui = ui
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
        self.ui.clear_screen()
        self.current_screen = 'start_screen'
        
        # Display start_screen unchanged things 
        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, 100, self.title_font_path)        # Title display
        
        # Options for start_screen
        self.option_names = ['Play', 'Setting', 'Credit', 'Quit'] 
        self.option_functions = [self.choose_map_screen_handle, self.show_setting, self.credit_screen_handle, self.exit_game]
        
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

        self.ui.update_screen()
        return options
    
    # ==========================
    #       Credit screen
    # ==========================
    
    def credit_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'credit_screen'
        # Display credit_screen unchanged things 
        self.ui.display_text_center("OUR MEMBER", self.ui.height // 10, self.ui.white, self.subtitle_font_size, self.text_font_path)        # Title display
                
        # Options for credit
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

        self.ui.update_screen()
        return options
    
    # ==========================
    # Choose map screen handle
    # ==========================
    
    def choose_map_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'choose_map_screen'
        # Display start_screen unchanged things 
        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, 100, self.title_font_path)        # Title display
                
        # Options for start_screen
        self.option_names = ['No obstacles', 'Obstacles', 'Return'] 
        self.option_functions = [self.update_choose_empty_map, self.update_choose_obstacles_map, self.go_back]
        
        # Menu and event handler
        options = self.update_choose_map_screen()
        return self.handle_events(self.update_choose_map_screen, options)

    def update_choose_empty_map(self):
        self.map_type = 'empty'
        return self.play_creen_handle
    
    def update_choose_obstacles_map(self):
        self.map_type = 'obstacles'
        return self.play_creen_handle
    
    def update_choose_map_screen(self, selected_option=0):
        # Options storage
        options = []
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10/4.5)
        
        # Options display
        for i in range(len(self.option_names)):
            color = self.ui.red if i == selected_option else self.ui.white
            options.append({
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding, first_opt_top_padding +  40 * i, color, self.text_font_size, self.text_font_path),
                'option_func': self.option_functions[i]
                })
    
        self.ui.update_screen()
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

    # ==========================
    #       Play screen
    # ==========================
    
    def play_creen_handle(self):
        obstacles_maps = ObstacleMap()
        obstacles = obstacles_maps.list_map[0]
        game_logic = AIPlayerGameLogic(obstacles, self.ui, (self.ui.rows // 2, self.ui.cols // 2))
        game_logic.game_loop()
         # if self.map_type == 'obstacles':
            
        
    def show_setting(self):
        return
                        
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
