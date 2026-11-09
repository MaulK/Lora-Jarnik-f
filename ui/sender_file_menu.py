from typing import Callable
from .ui_menu import UIMenu
from app.application import Application


class SenderFileMenu:
    __slots__ = ("want_to_move", "set_next_screen_fn", "application")

    set_next_screen_fn: Callable[[UIMenu], None]
    want_to_move: bool
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
            loaded_file_path_str = "None"
            loaded_file_path = self.application.get_loaded_file_path()
            if loaded_file_path != None:
                loaded_file_path_str = loaded_file_path

            print()
            print("=== SENDER FILE MENU ===")
            print()
            print("Loaded file:")
            print(loaded_file_path_str)
            print()
            print("What should system do?")
            print("1. Load File")
            print("2. Calculate CRC32")
            print("3. Send File")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                self._show_load_file_prompt()
            elif choice == "2":
                self._show_crc32()
            elif choice == "3":
                pass
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()

    def _show_load_file_prompt(self):
        print()
        filepath = input("File path:\n").strip()
        if filepath == "":
            print()
            print("Invalid file path. Operation aborted.")
            print()
            return
        print()
        try:
            self.application.load_file(filepath)
            print("File loaded.")
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"Unhandled error: {e}")
        print()
        input("Press Enter to continue...")

    def _show_crc32(self):
        print()
        try:
            crc32 = self.application.calculate_crc32_of_loaded_file()
            print("CRC32:")
            print(crc32)
        except FileNotFoundError:
            print("No loaded file. Please load file using option 1 first.")
        except Exception as e:
            print(f"Unhandled error: {e}")
        print()
        input("Press Enter to continue...")
