import pygame
from UI.window import *
from Logic.gamelogic import *
from menu import Menu

def main():
    pygame.init()

    base_ui = UI()

    menu = Menu(base_ui)

    menu.run_menu()

    pygame.quit()

if __name__ == "__main__":
    main()

