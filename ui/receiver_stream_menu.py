from typing import Callable
from .ui_menu import UIMenu


class ReceiverStreamMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn")

    def __init__(self, set_next_screen_fn: Callable[[UIMenu], None]):
        self.want_to_move = False
        self.set_next_screen_fn = set_next_screen_fn

    def show(self):
        self.want_to_move = False
        while not self.want_to_move:
            print()
            print("=== RECEIVER STREAM MENU ===")
            print()
            print("What should system do?")
            print("1. Listen Stream")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                pass
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.RECEIVER)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()
