import pygame
from Logic.gamelogic import *
from Logic.singlelogic import SinglePlayerGameLogic as HumanPlayerGameLogic
from Logic.ailogic import AIPlayerGameLogic
from obstacles import ObstacleMap
from UI.window import * 

class Menu:
    def __init__(self, ui):
        self.ui = ui
        self.current_screen = None
        self.snake_count = 0
        
        # Functional board variables in play screen
        self.functional_board_x = self.ui.grid_pos + self.ui.cols * self.ui.snake_block + 50
        self.functional_board_width = self.ui.width * 0.29
        
        self.button_witdh = self.functional_board_width // (10/3)
        self.small_button_width = self.button_witdh // 2
        self.button_padding = self.functional_board_width // (100/5)
        
        self.first_player_board_top_padding = self.ui.grid_pos + 90
        self.board_padding = 15
        
        self.speed_slider = Slider(self.functional_board_x + self.button_witdh + self.button_padding, self.ui.grid_pos + 50, self.button_witdh * 1.5, 1, 60, 30, self.ui.dark_green, self.ui.gray)
        
        # Options for each screen
        option_names = [] 
        option_functions = []

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
        self.current_screen = 'main'
        
        # Display start_screen unchanged things 
        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, self.ui.logo_font)        # Title display
        
        # Options for start_screen
        self.option_names = ['Play', 'Setting', 'Credit', 'Quit'] 
        self.option_functions = [self.play_creen_handle, self.show_setting, self.credit_screen_handle, self.exit_game]
        
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
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding, first_opt_top_padding +  40 * i, color, self.ui.text_font),
                'option_func': self.option_functions[i]
                })

        self.ui.update_screen()
        return options
    
    # ==========================
    #       Credit screen
    # ==========================
    
    def credit_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'credit'
        # Display credit_screen unchanged things 
        self.ui.display_text_center("OUR MEMBER", self.ui.height // 10, self.ui.white, self.ui.subtitle_font)        # Title display
                
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
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.ui.text_font),
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
        self.current_screen = 'play'
        
        # Load map
        self.map_list = [ set() ]
        obstacles_maps = ObstacleMap()
        self.map_list.extend( obstacles_maps.list_map)
        self.selected_map = 0
            
        # All player along with its need attributes (for example: algorithm box, check for AI or player)
        player_stuff_list = []
        
        # Handle loop
        is_clicked = False
        self.is_playing = False
        self.is_human_picked = False
        
        while True:
            # If user click on something
            # I prefer process event click on next frame
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_clicked:
                # Pause/Go which handled by is_playing
                if self.pause_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = not self.is_playing
                # Reset game
                if self.reset_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = False
                    self.is_human_picked = False
                    self.snake_count = 0
                    for _ in range(len(player_stuff_list)):
                        player = player_stuff_list.pop()
                        self.delete_player(player_stuff_list, player)
                        
                # Go back
                if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                    return self.go_back
                
                # Add player
                if self.add_human_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_human_picked = True
                    self.add_human_player(player_stuff_list)
                if self.add_ai_button_rect.collidepoint(mouse_x, mouse_y):
                    self.add_ai_player(player_stuff_list)

                # If delete a player
                for player_stuff in player_stuff_list:
                    if player_stuff['del'] and player_stuff['del'].collidepoint(mouse_x, mouse_y):
                        # If man player is deleted
                        if player_stuff['is_human']:
                            self.is_human_picked = False
                        self.delete_player(player_stuff_list, player_stuff)
                        
            is_clicked = False

            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    is_clicked = True
                    
                self.speed_slider.handle_event(event)
                for player_stuff in player_stuff_list:
                    # Handle for algorithm choice of AI
                    if player_stuff and not player_stuff['is_human']:
                        player_stuff['algo_cbb'].handle_event(event)
                    # Human play handle key stroke
                    elif player_stuff['is_human']:
                        player_stuff['player'].handle_events(event)
            
            # Only accept one action in 1 frame
            for player_stuff in player_stuff_list:
                if player_stuff['is_human']:
                    player_stuff['player'].is_changed_direction = False
            
            # Process for game
            if self.is_playing:
                 # Update temporary obstacles that not constant
                temp_obstacles = set()
                # Achieve obstacles 1st
                for player_stuff in player_stuff_list:
                    # It should be next snakes positions as ostacles
                    # If it's current --> may collision
                    # This is just current positions
                    temp_obstacles.update(player_stuff['player'].get_snake_as_obstacles())
                
                # Process all data first
                for player_stuff in player_stuff_list:
                    # Update temporary obstacles to process
                    player_stuff['player'].temp_obstacles = temp_obstacles.copy()
                    
                    # Update algorithm to process in case AI
                    if not player_stuff['is_human']:
                        player_stuff['player'].algorithm = player_stuff['player'].pathfinding.path_algorithm[player_stuff['algo_cbb'].selected]
    
                    player_stuff['player'].one_frame_data_process()
                    
                # Check for validation after process all data
                # Retrieve snake obstacles after process first
                temp_obstacles.clear()
                for player_stuff in player_stuff_list:
                    temp_obstacles.update(player_stuff['player'].get_snake_as_obstacles())
                
                # Update other snakes position for each snake (not inlucde itself)
                for player_stuff in player_stuff_list:
                    player_stuff['player'].temp_obstacles = temp_obstacles - player_stuff['player'].get_snake_as_obstacles()
                    
                # Check valid
                for player_stuff in player_stuff_list:
                    player_stuff['player'].check_validation()
                    # Check lose
                    if player_stuff['player'].game_over:
                        player_stuff['player'].handle_lose(f'{player_stuff['name']} has lost.')
                        # If human lose --> human can picked again
                        if player_stuff['is_human']:
                            self.is_human_picked = False
                        self.delete_player(player_stuff_list, player_stuff)
                    
            # Display frame
            self.ui.clear_screen()
            self.display_main_functional_board()
            self.display_player_functional_board(player_stuff_list)
            self.ui.draw_grid()
            self.ui.draw_obstacles(self.map_list[self.selected_map])
            
            # Update snake UI
            for player_stuff in player_stuff_list:                    
                player_stuff['player'].update_screen()     
            
            self.ui.clock.tick(self.speed_slider.get_value())
            self.ui.refresh_screen()
        
    def delete_player(self, player_list, player):
        if player['player'].snake_color:
            self.ui.return_snake_color(player['player'].snake_color)
        if player in player_list:
            player_list.remove(player)
    
    def add_human_player(self, player_list):
        player_list.append({
            'name': f'Snake {self.snake_count + 1}',
            'player': HumanPlayerGameLogic(self.map_list[self.selected_map], self.ui, (0, 0), self.ui.get_snake_color()),
            'is_human': True,
            'algo_cbb': None,
            'del': None
        })
        self.snake_count += 1
    
    def add_ai_player(self, player_list):
        algorithm = Pathfinding((self.ui.rows, self.ui.cols))
        player_list.append({
            'name': f'Snake{self.snake_count + 1}',
            'player': AIPlayerGameLogic(self.map_list[self.selected_map], self.ui, (0, 0), self.ui.get_snake_color()),
            'is_human': False,
            'algo_cbb': ComboBox(100, 23, algorithm.path_algorithm_names, self.ui.small_text_font, self.ui.white, self.ui.gray, self.ui.white, self.ui.dark_blue),
            'del': None
        })
        self.snake_count += 1
            
    def display_main_functional_board(self):
        """
        Main functional board
        """
        # Change map
        self.previous_map_button_rect = self.ui.display_image(self.functional_board_x - 40, self.ui.grid_pos, (30/128), r"assets/images/up-arrow.png")
        self.next_map_button_rect = self.ui.display_image(self.functional_board_x - 40, self.ui.grid_pos + self.ui.rows * self.ui.snake_block - 30, (30/128), r"assets/images/down-arrow.png")
        
        # Buttons
        self.pause_button_rect = self.ui.display_button((self.functional_board_x, self.ui.grid_pos), (self.button_witdh, 30), 'Stop' if self.is_playing else 'Go!', self.ui.text_font, self.ui.white, self.ui.dark_blue, radius=10)
        self.reset_button_rect = self.ui.display_button((self.functional_board_x + (self.button_witdh + self.button_padding), self.ui.grid_pos), (self.button_witdh, 30), 'Reset', self.ui.text_font, self.ui.white, self.ui.dark_blue, radius=10)
        self.back_button_rect = self.ui.display_button((self.functional_board_x + (self.button_witdh + self.button_padding) * 2, self.ui.grid_pos), (self.button_witdh, 30), 'Back', self.ui.text_font, self.ui.white, self.ui.red, radius=10)
        
        # Speed slider
        self.ui.display_text('Speed', self.functional_board_x + 13, self.ui.grid_pos + self.pause_button_rect.height + 10, self.ui.white, self.ui.text_font)
        self.speed_slider.draw(self.ui.screen)
        self.ui.display_text(str(self.speed_slider.get_value()), self.functional_board_x + (self.button_witdh + self.button_padding) * 2.45, self.ui.grid_pos + self.pause_button_rect.height + 13, self.ui.red, self.ui.text_font)
    
    def display_player_functional_board(self, player_stuff_list):
        """
        Each functional board of each snake
        """
        open_cbb_index = -1
        open_cbb_top_padd = 0
        for i, player_stuff in enumerate(player_stuff_list):
            back_board_top_padding = self.first_player_board_top_padding + (70 + self.board_padding) * i
            # Back board
            self.ui.display_button((self.functional_board_x, back_board_top_padding), (self.functional_board_width, 70), '', self.ui.text_font, self.ui.white, self.ui.dark_blue, radius=10)
            
            # Test information
            self.ui.display_text(f'{player_stuff['name']}-{player_stuff['player'].score}', self.functional_board_x + 13, back_board_top_padding + 10, self.ui.white, self.ui.text_font)
            
            # Player tag
            self.ui.display_button((self.functional_board_x + self.functional_board_width - 82, back_board_top_padding + 5), (30, 20), 'HM' if player_stuff['is_human'] else 'AI', self.ui.text_font_2, self.ui.gray, self.ui.light_blue, radius=10)
            
            # Delete player
            player_stuff['del'] = self.ui.display_button((self.functional_board_x + self.functional_board_width - 42, back_board_top_padding + 5), (30, 20), 'DEL', self.ui.text_font_2, self.ui.white, self.ui.red, radius=10)
            
            # AI information display
            if not player_stuff['is_human']:
                # Traveled count
                self.ui.display_text(f'P {player_stuff['player'].traveled_count}', self.functional_board_x + 16, back_board_top_padding + 40, self.ui.white, self.ui.small_text_font)
                
                # Draw unopen combo box first
                if not player_stuff['algo_cbb'].is_open:
                    player_stuff['algo_cbb'].draw(self.ui.screen, self.functional_board_x + 180, back_board_top_padding + 35)
                # If a combo box is open, save its index and draw later
                else:
                    open_cbb_index = i
                    open_cbb_top_padd = back_board_top_padding + 35
            
        # If a combobox is open, it should be drawn last
        if open_cbb_index != -1:
            player_stuff_list[open_cbb_index]['algo_cbb'].draw(self.ui.screen, self.functional_board_x + 180, open_cbb_top_padd)
               
        # Max player
        if (len(player_stuff_list) >= 5):
            return

        # Buttons to add player
        top_padding = self.first_player_board_top_padding + (70 + self.board_padding) * len(player_stuff_list)
        add_ai_button_left_padding = self.functional_board_x + self.functional_board_width // 2 - self.small_button_width // 2
        if not self.is_human_picked:
            self.add_human_button_rect = self.ui.display_button((add_ai_button_left_padding + self.small_button_width // 2 + 10, top_padding), (self.small_button_width, 15), '+Man', self.ui.small_text_font, self.ui.red, self.ui.light_red, radius=10)
            add_ai_button_left_padding -= (self.button_witdh // 4 + 10)
        self.add_ai_button_rect = self.ui.display_button((add_ai_button_left_padding, top_padding), (self.button_witdh // 2, 15), '+Bot', self.ui.small_text_font, self.ui.red, self.ui.light_red, radius=10)

    def show_setting(self):
        return