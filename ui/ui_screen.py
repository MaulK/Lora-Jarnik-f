from .main_menu import MainMenu
from .ui_menu import UIMenu
from .sender_menu import SenderMenu
from .sender_file_menu import SenderFileMenu
from .sender_stream_menu import SenderStreamMenu
from .receiver_menu import ReceiverMenu
from .receiver_file_menu import ReceiverFileMenu
from .receiver_stream_menu import ReceiverStreamMenu
from app.application import Application


class UIScreen:
    __slots__ = (
        "current_screen",
        "main_menu",
        "sender_menu",
        "sender_file_menu",
        "sender_stream_menu",
        "receiver_menu",
        "receiver_file_menu",
        "receiver_stream_menu",
    )

    current_screen: UIMenu
    main_menu: MainMenu
    sender_menu: SenderMenu
    sender_file_menu: SenderFileMenu
    sender_stream_menu: SenderStreamMenu
    receiver_menu: ReceiverMenu
    receiver_file_menu: ReceiverFileMenu
    receiver_stream_menu: ReceiverStreamMenu

    def __init__(self, application: Application):
        self.current_screen = UIMenu.MAIN
        self.main_menu = MainMenu(set_next_screen_fn=self._set_next_screen)
        self.sender_menu = SenderMenu(set_next_screen_fn=self._set_next_screen)
        self.sender_file_menu = SenderFileMenu(
            set_next_screen_fn=self._set_next_screen, application=application
        )
        self.sender_stream_menu = SenderStreamMenu(
            set_next_screen_fn=self._set_next_screen, application=application
        )
        self.receiver_menu = ReceiverMenu(set_next_screen_fn=self._set_next_screen)
        self.receiver_file_menu = ReceiverFileMenu(
            set_next_screen_fn=self._set_next_screen
        )
        self.receiver_stream_menu = ReceiverStreamMenu(
            set_next_screen_fn=self._set_next_screen, application=application
        )

    def _set_next_screen(self, target: UIMenu):
        self.current_screen = target

    def show(self):
        while self.current_screen != UIMenu.EXIT:
            if self.current_screen == UIMenu.MAIN:
                self.main_menu.show()
            elif self.current_screen == UIMenu.SENDER:
                self.sender_menu.show()
            elif self.current_screen == UIMenu.SENDER_FILE:
                self.sender_file_menu.show()
            elif self.current_screen == UIMenu.SENDER_STREAM:
                self.sender_stream_menu.show()
            elif self.current_screen == UIMenu.RECEIVER:
                self.receiver_menu.show()
            elif self.current_screen == UIMenu.RECEIVER_FILE:
                self.receiver_file_menu.show()
            elif self.current_screen == UIMenu.RECEIVER_STREAM:
                self.receiver_stream_menu.show()
