from typing import Callable
from .ui_menu import UIMenu
from app.application import Application
import time


class SenderStreamMenu:
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
            print("=== SENDER STREAM MENU ===")
            print()
            print("What should system do?")
            print("1. Send Stream")
            print("0. Back")
            print()

            choice = input("Your choice: ").strip()
            if choice == "1":
                self._show_stream_progress()
            elif choice == "0":
                self.want_to_move = True
                self.set_next_screen_fn(UIMenu.SENDER)
            else:
                print()
                print("!!! INVALID SELECTION !!!")
                print()

    def _show_stream_progress(self):
        print()
        print("Press Ctrl+C to stop. Stream will start on 3 seconds...")
        time.sleep(3)
        print()
        self.application.start_sending_stream_data(
            report_sending_data=self._print_sending_data
        )

    def _print_sending_data(self, current_data: int):
        print(f"Sending data: {current_data}")
