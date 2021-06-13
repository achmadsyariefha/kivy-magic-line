from logging import root
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
# from kivy.uix.recycleview import RecycleView
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.core.image import Image
from kivy.core.window import Window

## Window Size

Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)
Config.write()

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
class StartScreen(Screen):
    pass

# GameScreen
class GameScreen(Screen):
    pass

# RootScreen
class RootScreen(ScreenManager):
    pass

# Main
class MainApp(App):
    def build(self):
        return RootScreen()

if __name__ =="__main__":
    MainApp().run()