from logging import root
import kivy
from kivy import clock
from kivy import app
from kivy.logger import BLACK
from kivymd.uix import button
from kivymd.uix.behaviors import backgroundcolor_behavior
kivy.require('1.0.0')

from kivy.config import Config
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader, Sound
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

sound = ObjectProperty(None, allownone=True)

## Background Music
class BackgroundMusic(Sound):
    def __init__(self):
        self.sound = SoundLoader.load('resources/bgm/beach_party.mp3')

## Sound Effects
class SoundEffects(Sound):
    def __init__(self):
        self.sound = SoundLoader.load('resources/sfx/sample.mp3')

# StartScreen
class StartScreen(MDScreen):
    pass

# GameScreen
class GameScreen(MDScreen):
    grid = []
    isGameOver = False
    difficulty = ''
    clicked = False
    game_grid = ObjectProperty(None)
    # game_time = NumericProperty()
    # game_score = NumericProperty()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        color = 0
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.game_grid.cols = 10
        for i in range(100):
            board_row = MDBoxLayout(orientation = "horizontal", line_color= (0,0,0,0))
            board_button = Button(
                background_normal="",
                background_color=GameScreen.get_color(i)
                )
            board_button.bind(on_press = self.move_object)
            board_row.add_widget(board_button)
            self.game_grid.add_widget(board_row)

    def move_object(self, instance):
        if instance.state == 'down':
            self.clicked = True
        elif instance.state == 'normal':
            self.clicked = False
        print('Button', instance, 'has been', instance.state, 'clicked =', self.clicked)
    
    def get_color(i):
        return [1,1,1,0]

    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"

# SettingsScreen
class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.bgm_toggle = SoundToggle()

    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"

    def toggle_bgm(self, instance, value):
        if value:
            print('Switch is', instance.state, 'state')
        else:
            print('Switch is', instance.state, 'state')

    def on_sfx_slider_value(self, widget):
        # soundVolume = float(widget.value/100)
        # sound.volume = soundVolume
        print("Slider : "+ str(widget.value/100))

    def on_sfx_switch_value(self, widget):
        pass

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

# Toggle Sound
class SoundToggle(MDRectangleFlatButton, MDToggleButton):
    state = StringProperty(None)
    active = BooleanProperty(False)
    sound = ObjectProperty(None, allownone=True)
    def __init__(self, **kwargs):
        super(SoundToggle, self).__init__(**kwargs)
        self.background_down = (0, 0, 1, 1)
        self.font_color_down = [1, 0, 0, 1]
        self.font_size = "12sp"
        self.allow_no_selection = False
        self.sound = BackgroundMusic()
        self.bind(state = self.bgm_on_state)
        self.sfx = SoundEffects()

    def bgm_on_state(self, instance, value):
        if self.state == 'down':
            self.sound.play()
        else:
            self.sound.stop()

    def sfx_on_state(self, widget, value):
        if value == 'down':
            self.sfx.play()
        else:
            self.sfx.stop()

# Main
class MainApp(MDApp):

    dialog = None
    
    def build(self):
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        Config.write()
        Window.size = (400,600)
        Window.borderless = True
        Clock.max_iteration = 20
        self.title = "Magic Line"
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

# Player
class Player(object):
    name = ''
    score = 0
    time = 0
    turn = 0

    def __init__(self, name, score, time, turn):
        self.name = name
        self.score = score
        self.time = time
        self.turn = turn
        return

# GameBall
class GameBall(object):
    color = ''
    button = 0
    rows = 0
    column = 0

    def __init__(self, color, button, rows, column):
        self.color = color
        self.button = button
        self.rows = rows
        self.column = column
        return

class GameBoard(Widget):
    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)

class GameBoardColumn(Widget):
    def __init__(self, **kwargs):
        super(GameBoardColumn, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.magicLineGame = None

if __name__ =="__main__":
    MainApp().run()