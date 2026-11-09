from typing import Callable
from .ui_menu import UIMenu


class MainMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn")

    def __init__(self, set_next_screen_fn: Callable[[UIMenu], None]):
        self.want_to_move = False
        self.set_next_screen_fn = set_next_screen_fn

    def show(self):
        self.want_to_move = False
        while not self.want_to_move:
            print()
            print("=== MAIN MENU ===")
            print()
            print("Select your role:")
            print("1. Sender")
            print("2. Receiver")
            print("0. Exit")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER)
            elif choice == "2":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.RECEIVER)
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.EXIT)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()
