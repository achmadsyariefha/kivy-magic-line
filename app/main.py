import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.recycleview import RecycleView
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image
from kivy.core.window import Window

## Window Size

Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 600)
Config.write()

## Label

## class FirstKivy(App):
##    def build(self):
##        return Label(text='[u][color=ff0066][b]Better days[/b][/color] are coming; they are called [i][color=ff9933]Saturday[/i] and [i]Sunday[/i][/color][/i][/u]', markup= True)

## Button

## class KivyButton(App):
##    def build(self):
##        return Button(text="Test", pos=(300,350), size_hint=(.25, .18))

## FirstKivy().run()
## KivyButton().run()

## RecycleView

# Builder.load_string('''

# <ExampleRV>:
#     viewclass: 'Button'

#     RecycleBoxLayout:

#         size_hint_y: None

#         height: self.minimum_height

#         orientation: 'vertical'

# ''')

# class ExampleRV(RecycleView):
#     def __init__(self, **kwargs):
#         super(ExampleRV, self).__init__(**kwargs)
#         self.data = [{'text': str(x)} for (x) in range(20)]

# class RecycleApp(App):
#     def build(self):
#         return ExampleRV()

# RecycleApp().run()

class StartScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class RootScreen(ScreenManager):
    pass

# Main App

class MainApp(App):
    def build(self):
        return RootScreen()

if __name__ =="__main__":
    MainApp().run()