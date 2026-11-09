from typing import Callable
from .ui_menu import UIMenu


class SenderFileMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn")

    def __init__(self, set_next_screen_fn: Callable[[UIMenu], None]):
        self.want_to_move = False
        self.set_next_screen_fn = set_next_screen_fn

    def show(self):
        self.want_to_move = False
        while not self.want_to_move:
            print()
            print("=== SENDER FILE MENU ===")
            print()
            print("Loaded file: None")
            print()
            print("What should system do?")
            print("1. Load File")
            print("2. Calculate CRC32")
            print("3. Send File")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()
