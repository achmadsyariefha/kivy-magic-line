from logging import root
import kivy
from kivy import clock
from kivy import app
from kivy.logger import BLACK
from kivymd.uix.behaviors import backgroundcolor_behavior
kivy.require('1.0.0')

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
from kivy.core.audio import SoundLoader
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

## Window Size

Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)
Config.write()
Window.size = (400,600)
Clock.max_iteration = 20

## Background Music

sound = SoundLoader.load('resources/bgm/beach_party.mp3')
sound.play()

# StartScreen
class StartScreen(MDScreen):
    pass

# GameScreen
class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = GameBoard()
        self.add_widget(self.game)

    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"
        # MDApp.get_running_app().stop()

# SettingsScreen
class SettingsScreen(MDScreen):
    soundVolume = NumericProperty(0.0)

    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"

    def on_bgm_slider_value(self, widget):
        soundVolume = float(widget.value/100)
        sound.volume = soundVolume
        # print("Slider : "+ str(widget.value/100))

    def on_sfx_slider_value(self, widget):
        # soundVolume = float(widget.value/100)
        # sound.volume = soundVolume
        print("Slider : "+ str(widget.value/100))

    def on_checkbox_active(self, instance, value):
        if value:
            print('The checkbox', instance, 'is', value, 'and', instance.state, 'state')
        else:
            print('The checkbox', instance, 'is', value, 'and', instance.state, 'state')

# HelpScreen

class HelpScreen(MDScreen):
    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"
        

# RootScreen
class RootScreen(ScreenManager):
    pass

# Tile
class Tile(Widget):
    index = NumericProperty(0.0)
    source_image = StringProperty('')

# GameBoard
class GameBoard(Widget):
    game_board = ObjectProperty(None)
    def on_game_board(self, *args):
        if self.game_board:
            for x in range(10*10):
                self.game_board.add_widget(Tile(index=x))

# GameBall
# class GameBall(Image):
#     ball = ObjectProperty(None)

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

    # def boardGame(self, dt):
    #     board = MDApp.get_running_app().root.get_screen("game").ids.game_board
    #     for i in range(100):
    #         board_row = MDBoxLayout(orientation = "horizontal", line_color= (0,0,0,1))
    #         board_row.add_widget(Button(
    #             background_normal="",
    #             background_color=MainApp.get_color(i)
    #         ))
    #         board.add_widget(board_row)
    #     print ('call number'), dt
    
    # def start_game(self):
    #     self.clock_variable = None
    #     while self.clock_variable == None:
    #         self.clock_variable = Clock.schedule_once(self.boardGame, -1)

    # def get_color(i):
    #     return [1,1,1,1]

if __name__ =="__main__":
    MainApp().run()