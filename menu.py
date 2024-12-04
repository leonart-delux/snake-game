import pygame
from Logic.gamelogic import *
from Logic.singlelogic import SinglePlayerGameLogic as HumanPlayerGameLogic
from Logic.ailogic import AIPlayerGameLogic
from UI.obstacles import ObstacleMap
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
        
        self.speed_slider = Slider(self.functional_board_x + self.button_witdh + self.button_padding, self.ui.grid_pos + 50, self.button_witdh * 1.5, 1, 100, 30, self.ui.dark_green, self.ui.gray)

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

    def go_back(self):
        if self.current_screen == 'map_view' or self.current_screen == 'map_cre':
            return self.map_screen_handle
        
        if self.current_screen == 'play' or self.current_screen == 'sandbox':
            return self.choose_mode_screen_handle
        
        return self.start_screen_handle
  
    # ==========================
    #       Start screen
    # ==========================
    
    def start_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'start'

        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, self.ui.logo_font)        # Title display
        
        # Options for start
        options = list()
        option_names = ['Play', 'Map', 'Credit', 'Quit'] 
        
        # Options storage
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10/4)
        is_clicked = False
        
        while True:
            
            hoving_option = -1

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
            
            if is_clicked and options[0].collidepoint(mousex, mousey):
                # Start
                return self.choose_mode_screen_handle
                
            if is_clicked and options[1].collidepoint(mousex, mousey):
                # Map
                return self.map_screen_handle
            
            if is_clicked and options[2].collidepoint(mousex, mousey):
                # Credit 
                return self.credit_screen_handle
            
            if is_clicked and options[3].collidepoint(mousex, mousey):
                return self.exit_game()
            
            is_clicked = False

            # Options display
            options.clear()
            for i in range(len(option_names)):
                color = self.ui.red if i == hoving_option else self.ui.white
                options.append(self.ui.display_text(option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.ui.text_font))
                
            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()   
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True
    
            self.ui.update_screen()
    
    # ==========================
    #       Credit screen
    # ==========================
    
    def credit_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'credit'

        self.ui.display_text_center("OUR MEMBER", self.ui.height // 10, self.ui.white, self.ui.subtitle_font)        # Title display
        
        # Options for credit
        options = list()
        option_names = ['22110031 Bien Xuan Huy', '22110032 Le Gia Huy', '22110037 Nguyen Tien Huy', '22110085 Nguyen Truong', 'Return'] 
        
        # For options display
        option_left_padding = self.ui.width // 6
        first_opt_top_padding = self.ui.height // 3
        img_x = self.ui.width // (5/3)
        img_y = self.ui.height // 3.5
        
        image_paths = [ r'assets/images/mem_xhuy.png', r'assets/images/mem_ghuy.png', r'assets/images/mem_thuy.png', r'assets/images/mem_ntruong.png', r'assets/images/empty_border.png' ]
        selected_option = 0
        is_clicked = False
        
        while True:
            
            hoving_option = -1

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
                if is_clicked and options[i].collidepoint(mousex, mousey):
                    selected_option = i
            
            if is_clicked and options[4].collidepoint(mousex, mousey):
                return self.go_back()
            
            is_clicked = False

            # Options display
            options.clear()
            for i in range(len(option_names)):
                if i == hoving_option:
                    color = self.ui.red
                elif i == selected_option:
                    color = self.ui.blue
                else:
                    color = self.ui.white
                options.append(self.ui.display_text(option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.ui.text_font))
            
            # Fill old image (if appeared)
            self.ui.screen.fill((0, 0, 0), (img_x, img_y, 200, 300))
            self.ui.display_image(img_x, img_y, 0.7, image_paths[selected_option])
            
            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()   
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True
    
            self.ui.update_screen()

    # ==========================
    #       Mode screen
    # ==========================

    def choose_mode_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'choose_mode'

        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, self.ui.logo_font)        # Title display
        
        # Options for map
        options = list()
        option_names = ['Normal', 'Sandbox', 'Back'] 
    
        # For option display
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10/4)
        is_clicked = False
        
        while True:
            
            hoving_option = -1

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
            
            if is_clicked and options[0].collidepoint(mousex, mousey):
                # Map view
                return self.play_screen_handle
                
            if is_clicked and options[1].collidepoint(mousex, mousey):
                # Map edit
                return self.sandbox_screen_handle
            
            if is_clicked and options[2].collidepoint(mousex, mousey):
                return self.go_back()
            
            is_clicked = False

            # Options display
            options.clear()
            for i in range(len(option_names)):
                color = self.ui.red if i == hoving_option else self.ui.white
                options.append(self.ui.display_text(option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.ui.text_font))
                
            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()   
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True
    
            self.ui.update_screen()

    # ==========================
    #       Play screen
    # ==========================
    
    def play_screen_handle(self):
        self.current_screen = 'play'
        
        # Load map
        obstacles_maps = ObstacleMap()
        self.map_obstacles_list = obstacles_maps.list_map
        self.map_grid_size_list = obstacles_maps.list_gridsize
        self.selected_map = 0
        self.ui.define_grid(self.map_grid_size_list[self.selected_map])
            
        # All player along with its need attributes (for example: algorithm box, check for AI or player)
        player_stuff_list = []
        
        # Handle loop
        is_clicked = False
        self.is_playing = False
        self.is_human_picked = False
        
        # Hold temporary obstacles position on map
        # It's snakes positions
        # At first no snake --> empty
        temp_obstacles = set()
        
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
                    self.reset_game(player_stuff_list)

                # Go back
                if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = False
                    return self.go_back
                
                # Add player
                if self.add_human_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_human_picked = True
                    self.add_human_player(player_stuff_list)
                if self.add_ai_button_rect.collidepoint(mouse_x, mouse_y):
                    self.add_ai_player(player_stuff_list)
                
                # Change map
                if self.previous_map_button_rect.collidepoint(mouse_x, mouse_y):
                    direction = -1
                elif self.next_map_button_rect.collidepoint(mouse_x, mouse_y):
                    direction = 1
                else:
                    direction = 0
                if direction != 0:
                    self.selected_map = (self.selected_map + direction) % len(self.map_obstacles_list)
                    self.reset_game(player_stuff_list)
                    self.ui.define_grid(self.map_grid_size_list[self.selected_map])


                # If delete a player
                for player_stuff in player_stuff_list:
                    if player_stuff['del'] and player_stuff['del'].collidepoint(mouse_x, mouse_y):
                        # If man player is deleted
                        if player_stuff['is_human']:
                            self.is_human_picked = False
                        temp_obstacles = temp_obstacles - player_stuff['player'].get_snake_as_obstacles()
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
                    if player_stuff and not player_stuff['is_human'] and is_clicked:
                        player_stuff['algo_cbb'].handle_event(event)
                        is_clicked = True
                    # Human play handle key stroke
                    elif player_stuff['is_human']:
                        player_stuff['player'].handle_events(event)
            
            
            # Only accept one action in 1 frame
            # In previous step if a key is stroke for human player and successfully change direction
            # is_changed_direction changes to true
            # This one to reset to false
            for player_stuff in player_stuff_list:
                if player_stuff['is_human']:
                    player_stuff['player'].is_changed_direction = False
                    break
                    
            # Process for game
            # Initilization
            for player_stuff in player_stuff_list:
                # Havent initialized
                if not player_stuff['player'].is_initialized:
                    # Assign current map temporary obstacles
                    player_stuff['player'].temp_obstacles = temp_obstacles
                    # Initialize state including snake and food position
                    player_stuff['player'].initialize()
                    # Update this snake and food to temp obstacles list
                    temp_obstacles.update(player_stuff['player'].get_snake_as_obstacles())
            
            if self.is_playing:          
                # Process all data first
                for player_stuff in player_stuff_list:
                    # Update temporary obstacles to process
                    player_stuff['player'].temp_obstacles = temp_obstacles.copy()
                    
                    # Update algorithm to process in case AI
                    if not player_stuff['is_human']:
                        player_stuff['player'].algorithm = player_stuff['player'].pathfinding.path_algorithm[player_stuff['algo_cbb'].selected]
    
                    player_stuff['player'].one_frame_data_process(len(player_stuff_list) == 1)
                    
                # Update other snakes position for each snake (not inlucding itself) after process all data  
                player_stuff = None
                for player_stuff in player_stuff_list:
                    # Create new map temporary obstacles
                    # We need this set after last loop
                    temp_obstacles.clear()
                    # For each other snake
                    for other_player_stuff in player_stuff_list:
                        # Ignore current main snake
                        if (player_stuff != other_player_stuff):
                            # Add each other snake obstacles to temp_obstacles
                            temp_obstacles.update(other_player_stuff['player'].get_snake_as_obstacles())
                     
                    # Add total
                    player_stuff['player'].temp_obstacles = temp_obstacles.copy()
                
                # Temp obstacles in this session
                if player_stuff:
                    temp_obstacles.update(player_stuff['player'].get_snake_as_obstacles())
                        
            # Display frame
            self.ui.clear_screen()
            self.display_main_functional_board()
            self.display_player_functional_board(player_stuff_list)
            self.ui.draw_grid()
            self.ui.draw_obstacles(self.map_obstacles_list[self.selected_map])
            
            # Update snake UI
            for player_stuff in player_stuff_list:                    
                player_stuff['player'].update_screen()  
                
            self.ui.refresh_screen()
            
            if self.is_playing:
                # Check valid
                for player_stuff in player_stuff_list:
                    player_stuff['player'].check_validation()
                    # Check lose
                    if player_stuff['player'].game_over:
                        player_stuff['player'].handle_lose(f'{player_stuff['name']} has lost.')
                        # If human lose --> human can picked again
                        if player_stuff['is_human']:
                            self.is_human_picked = False
                        temp_obstacles = temp_obstacles - player_stuff['player'].get_snake_as_obstacles()
                        self.delete_player(player_stuff_list, player_stuff)
            
            self.ui.clock.tick(self.speed_slider.get_value())
    
    def reset_game(self, player_stuff_list):
        self.is_playing = False
        self.is_human_picked = False
        self.snake_count = 0
        for _ in range(len(player_stuff_list)):
            player = player_stuff_list.pop()
            self.delete_player(player_stuff_list, player)
    
    def delete_player(self, player_list, player):
        if player in player_list:
            player_list.remove(player)
    
    def add_human_player(self, player_list):
        player_list.append({
            'name': f'Snake{self.snake_count + 1}',
            'player': HumanPlayerGameLogic(self.map_obstacles_list[self.selected_map], self.ui, self.ui.get_snake_color()),
            'is_human': True,
            'algo_cbb': None,
            'del': None
        })
        self.snake_count += 1
    
    def add_ai_player(self, player_list):
        algorithm = Pathfinding((self.ui.rows, self.ui.cols))
        player_list.append({
            'name': f'Snake{self.snake_count + 1}',
            'player': AIPlayerGameLogic(self.map_obstacles_list[self.selected_map], self.ui, self.ui.get_snake_color()),
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
            self.ui.display_button((self.functional_board_x, back_board_top_padding), (self.functional_board_width, 70), '', self.ui.text_font, self.ui.white, player_stuff['player'].snake_color, radius=10)
            
            # Test information
            self.ui.display_text(f'{player_stuff['name']}-{player_stuff['player'].score}', self.functional_board_x + 13, back_board_top_padding + 10, self.ui.white, self.ui.text_font)
            
            # Player tag
            self.ui.display_button((self.functional_board_x + self.functional_board_width - 82, back_board_top_padding + 5), (30, 20), 'HM' if player_stuff['is_human'] else 'AI', self.ui.text_font_2, self.ui.gray, self.ui.light_blue, 1, 10, self.ui.gray)
            
            # Delete player
            player_stuff['del'] = self.ui.display_button((self.functional_board_x + self.functional_board_width - 42, back_board_top_padding + 5), (30, 20), 'DEL', self.ui.text_font_2, self.ui.white, self.ui.red, 1, 10, self.ui.gray)
            
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

    # ==========================
    #       Sandbox screen
    # ==========================
    
    def sandbox_screen_handle(self):
        self.current_screen = 'sandbox'
        
        # Load map
        obstacles_maps = ObstacleMap()
        self.map_obstacles_list = obstacles_maps.list_map
        self.map_grid_size_list = obstacles_maps.list_gridsize
        self.selected_map = 0
        self.ui.define_grid(self.map_grid_size_list[self.selected_map])
            
        # All player along with its need attributes (for example: algorithm box, check for AI or player)
        player_stuff_list = []
        # Algorithm to use
        algorithm = Pathfinding((self.ui.rows, self.ui.cols))
        algorithmCbb = ComboBox(self.functional_board_width, 30, algorithm.path_algorithm_names, self.ui.text_font, self.ui.white, self.ui.gray, self.ui.white, self.ui.dark_blue)
        # Max snake
        max_snake_slider = Slider(self.functional_board_x, self.ui.grid_pos + 120, self.functional_board_width, 1, 10, 3, self.ui.yellow, self.ui.gray)

        
        # Handle loop
        is_clicked = False
        self.is_playing = False
        is_started = False
        
        # Hold temporary obstacles position on map
        # It's snakes positions
        # At first no snake --> empty
        temp_obstacles = set()
        
        while True:
            # If user click on something
            # I prefer process event click on next frame
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if is_clicked:
                # Pause/Go which handled by is_playing
                if self.pause_button_rect.collidepoint(mouse_x, mouse_y):
                    self.is_playing = not self.is_playing
                    is_started = True
                # Reset game
                if self.reset_button_rect.collidepoint(mouse_x, mouse_y):
                    self.reset_game(player_stuff_list)
                    is_started = False
                    
                # Go back
                if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                    return self.go_back
                                
                # Change map
                if not is_started:
                    if self.previous_map_button_rect.collidepoint(mouse_x, mouse_y):
                        direction = -1
                    elif self.next_map_button_rect.collidepoint(mouse_x, mouse_y):
                        direction = 1
                    else:
                        direction = 0

                    if direction != 0:
                        self.selected_map = (self.selected_map + direction) % len(self.map_obstacles_list)
                        self.reset_game(player_stuff_list)
                        self.ui.define_grid(self.map_grid_size_list[self.selected_map])
                        algorithm.numb_rows, algorithm.numb_cols = self.ui.rows, self.ui.cols

            is_clicked = False
                    
            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    is_clicked = True
                    
                self.speed_slider.handle_event(event)
                if not is_started:
                    max_snake_slider.handle_event(event)
                    algorithmCbb.handle_event(event)
                     
            # Process for game
            
            # Started
            # Add snake to max snake
            if is_started:
                while len(player_stuff_list) < max_snake_slider.get_value():
                    self.add_ai_player(player_stuff_list)
                    # Add selected algorithm
                    player_stuff_list[len(player_stuff_list) - 1]['player'].algorithm = algorithm.path_algorithm[algorithmCbb.selected]
            
            # Initilization
            for player_stuff in player_stuff_list:
                # Havent initialized
                if not player_stuff['player'].is_initialized:
                    # Initialize state including snake and food position
                    player_stuff['player'].initialize()
            
            if self.is_playing:          
                # Update other NEXT snakes position for each snake (not inlucding itself) before process all data  
                for player_stuff in player_stuff_list:
                    # Create new map temporary obstacles
                    temp_obstacles.clear()
                    # For each other snake
                    for other_player_stuff in player_stuff_list:
                        # Ignore current main snake
                        if (player_stuff != other_player_stuff):
                            # Add each other snake obstacles to temp_obstacles
                            temp_obstacles.update(other_player_stuff['player'].get_next_snake_image_as_ostacles())
                    # Add self position
                    temp_obstacles.update(player_stuff['player'].get_snake_as_obstacles())
                    # Add total
                    player_stuff['player'].temp_obstacles = temp_obstacles.copy()
                
                # Process all data first
                for player_stuff in player_stuff_list:
                    player_stuff['player'].one_frame_data_process()
                    
                # Update other snakes position for each snake (not inlucding itself) after process all data  
                player_stuff = None
                for player_stuff in player_stuff_list:
                    # Create new map temporary obstacles
                    temp_obstacles.clear()
                    # For each other snake
                    for other_player_stuff in player_stuff_list:
                        # Ignore current main snake
                        if (player_stuff != other_player_stuff):
                            # Add each other snake obstacles to temp_obstacles
                            temp_obstacles.update(other_player_stuff['player'].get_snake_as_obstacles())
                    # Add total
                    player_stuff['player'].temp_obstacles = temp_obstacles.copy()
                        
            # Display frame
            self.ui.clear_screen()
            self.display_main_functional_board()
            self.ui.draw_grid()
            self.ui.draw_obstacles(self.map_obstacles_list[self.selected_map])
            
            # Display point
            if is_started:
                for i, player_stuff in enumerate(player_stuff_list):
                    back_board_top_padding = self.first_player_board_top_padding + 40 * i
                    self.ui.display_text(f'{player_stuff['name']}-{player_stuff['player'].score}', self.functional_board_x, back_board_top_padding + 10, player_stuff['player'].snake_color, self.ui.text_font)
                    self.ui.display_text(f'P {player_stuff['player'].traveled_count}', self.functional_board_x + 200, back_board_top_padding + 13, self.ui.white, self.ui.small_text_font)
            
            # Handle before start
            # If start, this game have to reset to this again
            if not is_started:
                # Show max snake adjust
                self.ui.display_text('Max snake', self.functional_board_x + 5, self.ui.grid_pos + 90, self.ui.white, self.ui.text_font)
                max_snake_slider.draw(self.ui.screen)
                self.ui.display_text(str(max_snake_slider.get_value()), self.functional_board_x + 160, self.ui.grid_pos + 90, self.ui.white, self.ui.text_font)
                max_snake_slider.draw(self.ui.screen)
                
                # Show algo to use
                self.ui.display_text('Algorithm', self.functional_board_x + 5, self.ui.grid_pos + 140, self.ui.white, self.ui.text_font)
                algorithmCbb.draw(self.ui.screen, self.functional_board_x, self.ui.grid_pos + 170)    
            
            # Update snake UI
            for player_stuff in player_stuff_list:                    
                player_stuff['player'].update_screen()  
                
            self.ui.refresh_screen()
            
            if self.is_playing:
                # Check valid
                for player_stuff in player_stuff_list:
                    player_stuff['player'].check_validation()
                    # Check lose
                    if player_stuff['player'].game_over:
                        # Remove snake in current screen temp obstacles
                        temp_obstacles = temp_obstacles - player_stuff['player'].get_snake_as_obstacles()
                        self.delete_player(player_stuff_list, player_stuff)
            
            self.ui.clock.tick(self.speed_slider.get_value())
    
    
    # ==========================
    #       Map screen
    # ==========================
    
    def map_screen_handle(self):
        self.ui.clear_screen()
        self.current_screen = 'map'

        self.ui.display_image(self.ui.width // (10/4.5), self.ui.height // 3.5, 0.6, r"assets/images/main_thumb.png")   # Thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, self.ui.logo_font)        # Title display
        
        # Options for map
        options = list()
        option_names = ['Map view', 'Create map', 'Back'] 
    
        # For option display
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10/4)
        is_clicked = False
        
        while True:
            
            hoving_option = -1

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
            
            if is_clicked and options[0].collidepoint(mousex, mousey):
                # Map view
                return self.map_view_screen_handle
                
            if is_clicked and options[1].collidepoint(mousex, mousey):
                # Map edit
                return self.map_edit_screen_handle
            
            if is_clicked and options[2].collidepoint(mousex, mousey):
                return self.go_back()
            
            is_clicked = False
            

            # Options display
            options.clear()
            for i in range(len(option_names)):
                color = self.ui.red if i == hoving_option else self.ui.white
                options.append(self.ui.display_text(option_names[i], option_left_padding, first_opt_top_padding +  35 * i, color, self.ui.text_font))
                
            # Handle event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()   
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True
    
            self.ui.update_screen()
    
    def map_edit_screen_handle(self):
        self.current_screen = 'map_cre'  
         
        # Options for map_editor_screen
        options = list()
        option_names = ['Clear', 'Save', 'Back'] 
        grid_slider = Slider(self.functional_board_x + self.functional_board_width * 0.05, self.ui.grid_pos + 110, self.functional_board_width * 0.9, 5, 40, 15, self.ui.purple, self.ui.white)
        
        # New map handle
        new_obstacles = set()
        new_size = 15
        
        # Display old map
        map_storage = ObstacleMap()

        option_top_padding = self.ui.grid_pos + self.ui.rows * self.ui.snake_block - 30
        is_clicked = False
        draw_mode = True    # true -> draw ; false -> erase
        is_dragging = False     # draw and erase mode
  
        while True:
            self.ui.clear_screen()
            
            hoving_option = -1
            new_size = grid_slider.get_value()

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
            
            if is_clicked and options[0].collidepoint(mousex, mousey):
                # Clear
                new_obstacles.clear()
                
            if is_clicked and options[1].collidepoint(mousex, mousey):
                # Save
                map_storage.add_map(new_obstacles, new_size)
            
            if is_clicked and options[2].collidepoint(mousex, mousey):
                return self.go_back()
            
            # Draw, Erase
            if is_dragging:
                # Get grid row and col based on mouse position (may wrong, check later)
                row, col = self.ui.get_cell_pos_in_grid(mousex, mousey)
                # Check if mouse is in grid or not
                if 0 <= row < self.ui.rows and 0 <= col < self.ui.cols:
                    if draw_mode:
                        new_obstacles.add((row, col))
                        
                    # Erase
                    elif (row, col) in new_obstacles:
                        new_obstacles.remove((row, col)) 
            
            is_clicked = False

            # Text display
            self.ui.display_button((self.functional_board_x, self.ui.grid_pos), (self.functional_board_width, 50), 'Map Editor', self.ui.subtitle_font, self.ui.dark_brown, self.ui.light_brown, 2, 20, self.ui.dark_brown)
            self.ui.display_text('Grid size:', self.functional_board_x + 15, self.ui.grid_pos + 75, self.ui.white, self.ui.text_font)
            self.ui.display_text(str(grid_slider.get_value()), self.functional_board_x + self.functional_board_width - 40, self.ui.grid_pos + 75, self.ui.white, self.ui.text_font)
            
            # Grid size slider
            grid_slider.draw(self.ui.screen)
            
            # Instructions
            self.ui.display_text('Mode: Draw' if draw_mode else 'Mode: Erase', self.functional_board_x + 15, self.ui.grid_pos + 160, self.ui.white, self.ui.text_font)
            self.ui.display_text('E to Erase..', self.functional_board_x + 25, self.ui.grid_pos + 190, self.ui.yellow, self.ui.funny_font)
            self.ui.display_text('D to Draw!!', self.functional_board_x + 25, self.ui.grid_pos + 260, self.ui.green, self.ui.funny_font)

            # Option display
            options.clear()
            for i in range(len(option_names)):
                color = self.ui.blue if i != hoving_option else self.ui.red
                options.append(self.ui.display_text(option_names[i], self.functional_board_x + 110 * i, option_top_padding, color, self.ui.subtitle_font_2))

            # Display
            self.ui.define_grid(grid_slider.get_value())
            self.ui.draw_grid()
            self.ui.draw_obstacles(new_obstacles)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True
                    is_dragging = True
                
                # Unhold left click
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    is_dragging = False
                    
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        draw_mode = True
                    elif event.key == pygame.K_e:
                        draw_mode = False                
                    
                grid_slider.handle_event(event)
            
            self.ui.update_screen()
            self.ui.clock.tick(30)
    
    def map_view_screen_handle(self):
        self.current_screen = 'map_view'  
         
        # Options for map_view_screen
        options = list()
        option_names = ['Delete', 'Back'] 

        # Display old map
        map_storage = ObstacleMap()
        selected_map = 0
        previous_map_button_rect = next_map_button_rect = None
        top_button_padding = self.ui.grid_pos + self.ui.rows * self.ui.snake_block - 30

        # For option display
        option_top_padding = self.ui.grid_pos + self.ui.rows * self.ui.snake_block - 30
        is_clicked = False
  
        while True:
            self.ui.clear_screen()
            
            hoving_option = -1

            # Option event
            mousex, mousey = pygame.mouse.get_pos()
            
            for i in range(len(options)):
                if options[i] and options[i].collidepoint(mousex, mousey):
                    hoving_option = i
            
            if is_clicked and options[0].collidepoint(mousex, mousey) and len(map_storage.list_map) > 1:
                # Clear
                map_storage.del_map(selected_map)
                selected_map = 0
                
            if is_clicked and options[1].collidepoint(mousex, mousey):
                # Back
                return self.go_back()

            if is_clicked and previous_map_button_rect.collidepoint(mousex, mousey):
                selected_map = (selected_map - 1) % len(map_storage.list_map)
            
            if is_clicked and next_map_button_rect.collidepoint(mousex, mousey):
                selected_map = (selected_map + 1) % len(map_storage.list_map)
            
            is_clicked = False

            # Text display
            self.ui.display_button((self.functional_board_x, self.ui.grid_pos), (self.functional_board_width, 50), 'MAP VIEW', self.ui.funny_font, self.ui.white, self.ui.red, radius = 20)

            # Option display
            options.clear()
            for i in range(len(option_names)):
                color = self.ui.blue if i != hoving_option else self.ui.red
                options.append(self.ui.display_text(option_names[i], self.functional_board_x + 120 + 110 * i, option_top_padding, color, self.ui.subtitle_font_2))
            
             # Change map
            previous_map_button_rect = self.ui.display_image(self.functional_board_x - 40, self.ui.grid_pos, (30/128), r"assets/images/up-arrow.png")
            next_map_button_rect = self.ui.display_image(self.functional_board_x - 40, top_button_padding, (30/128), r"assets/images/down-arrow.png")

            # Display
            self.ui.define_grid(map_storage.list_gridsize[selected_map])
            self.ui.draw_grid()
            self.ui.draw_obstacles(map_storage.list_map[selected_map])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    is_clicked = True                           
            
            self.ui.update_screen()
            self.ui.clock.tick(30)
        
                