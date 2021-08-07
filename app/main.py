from logging import root
import kivy
from kivy import clock
from kivy import app
from kivy.logger import BLACK
from kivymd.uix.behaviors import backgroundcolor_behavior
kivy.require('2.0.0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

## Window Size

Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)
Config.write()
Window.size = (400,600)
Clock.max_iteration = 20

# class Game(BoxLayout):
#     label_text = StringProperty()
#     def __init__(self, **kwargs):
#         super(Game, self).__init__(**kwargs)
#         self.count = 0
#         self.label_text = str(self.count)

#     def increment(self, *args):
#         self.count += 1
#         self.label_text = str(self.count)
#         print (self.label_text)

# StartScreen
class StartScreen(MDScreen):
    pass

# GameScreen
class GameScreen(MDScreen):
    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"
        MainApp.run_game.cancel()

# SettingsScreen
class SettingsScreen(MDScreen):
    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"


# RootScreen
class RootScreen(ScreenManager):
    pass
    
def boardGame(self):
    board = MDApp.get_running_app().root.get_screen("game").ids.game_board
    for i in range(10):
        board_row = MDBoxLayout(orientation = "horizontal", line_color= (0,0,0,1))
        for j in range(10):
            board_row.add_widget(Button(
                background_normal="",
                background_color=MainApp.get_color(i, j),
                border = (0, 16, 0, 16)
            ))

        board.add_widget(board_row)

# Main
class MainApp(MDApp):
    dialog = None

    def build(self):
        return RootScreen()

    def show_exit_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title ="Exit",
                text = "Are You Sure you want to exit ?",
                buttons = [
                    MDFlatButton(
                        text="YES", text_color= self.theme_cls.primary_color, on_press = self.stop
                    ),
                    MDFlatButton(
                        text="NO", text_color= self.theme_cls.primary_color, on_press = self.close_dialog
                    )
                ]
            )
        self.dialog.open()

    def close_dialog(self, inst):
        self.dialog.dismiss()
    
    run_game = Clock.create_trigger(boardGame)
    


    # def on_start(self):
    #     board = self.root.get_screen("game").ids.game_board
    #     for i in range(5):
    #         board_row = MDBoxLayout(orientation = "horizontal", line_color= (0,0,0,1))
    #         for j in range(10):
    #             board_row.add_widget(Button(
    #                 background_normal="",
    #                 background_color=self.get_color(i, j),
    #                 border = (0, 16, 0, 16)
    #             ))

    #         board.add_widget(board_row)

    def get_color(i ,j):
        return [1,1,1,1]

    def on_checkbox_active(self, instance, value):
        if value:
            print('The checkbox', instance, 'is active', 'and', instance.state, 'state')
        else:
            print('The checkbox', instance, 'is inactive', 'and', instance.state, 'state')

if __name__ =="__main__":
    MainApp().run()