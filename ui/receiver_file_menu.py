from typing import Callable
from .ui_menu import UIMenu
from app.application import Application


class ReceiverFileMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn", "application")

    want_to_move: bool
    set_next_screen_fn: Callable[[UIMenu], None]
    application: Application

    def __init__(
        self, set_next_screen_fn: Callable[[UIMenu], None], application: Application
    ):
        self.want_to_move = False
        self.set_next_screen_fn = set_next_screen_fn
        self.application = application

    def show(self):
        self.want_to_move = False
        while not self.want_to_move:
            print()
            print("=== RECEIVER FILE MENU ===")
            print()
            print("Received file:")
            received_file_path_str = "None"
            if self.application.received_file != None:
                received_file_path_str = self.application.received_file.path
            print(received_file_path_str)
            print()
            print("What should system do?")
            print("1. Receive File")
            print("2. Calculate CRC32")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                self._show_receive_file()
            elif choice == "2":
                pass
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.RECEIVER)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()

    def _show_receive_file(self):
        print()
        print("Press Ctrl+C to cancel. Receiving file...")
        print()
        self.application.start_receiving_file()
        print("File received.")
        print()
        input("Press enter to continue...")
