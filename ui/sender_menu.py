from typing import Callable
from .ui_menu import UIMenu


class SenderMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn")

    def __init__(self, set_next_screen_fn: Callable[[UIMenu], None]):
        self.want_to_move = False
        self.set_next_screen_fn = set_next_screen_fn

    def show(self):
        self.want_to_move = False
        while not self.want_to_move:
            print()
            print("=== SENDER MENU ===")
            print()
            print("What will you send?")
            print("1. File")
            print("2. Stream Data")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER_FILE)
            elif choice == "2":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER_STREAM)
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.MAIN)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()
