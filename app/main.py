from math import sqrt
from random import randint
from core import Ball, Player

import kivy

kivy.require('1.0.0')

from kivy.config import Config
from kivy.clock import Clock, ClockEvent
from kivy.core.window import Window
from kivy.core.audio import SoundLoader, Sound
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, BooleanProperty

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.dialog import MDDialog

from algorithm import astar

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
    players = {}
    dynamic_value = 10
    grid = []
    is_game_over = False
    destroyed = False
    prev_ball = ''
    prev_color = ''
    difficulty = ''
    layout = ''
    board_layout = ''
    turn = 'pl'
    count = 0
    clicked = False

    time_label = StringProperty()
    
    # game_time = NumericProperty()
    # game_score = NumericProperty()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.event = Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.layout = self.ids.board_one
        self.dynamic_value = 10
        grid_value = self.dynamic_value * self.dynamic_value
        diviser = int(sqrt(grid_value))
        self.board_layout = GridLayout(cols = self.dynamic_value, rows = self.dynamic_value)
        nbBalls = int((self.dynamic_value / 2) * ((self.dynamic_value / 2 )- 1))
        self.players['pl'] = Player(name = 'Player', player = 'pl', score = nbBalls)
        color = 0
        counter = 0
        jumpline = 0
        for i in range(0, grid_value):
            if jumpline != int(i/ diviser):
                jumpline += 1
                counter += 1
            try:
                value = self.grid[int(i / (diviser * (i % diviser)))]
            except Exception as e:
                self.grid.append([])
            button_id = str(int(i / diviser)) + '-' + str(int(i % diviser))
            ball = ''
            # if add_ball <= 3:
            #     color = (0.75, 0.58, 0.36, 2.5)
            #     # if i < int(nbBalls * 2):
            #     #     ball = 'pl'
            #     ball = 'pl'
            # else:
            #     color = (0.84, 0.70, 0.49, 2.5)
            if counter % randint(1, 10) != 0:
                if i < int(nbBalls * 2):
                    color = randint(1, 9)
                    ball = 'pl'
            else:
                color = 0
            y = int(i / diviser)
            x = int(i % diviser)
            self.grid[y].append([])
            self.grid[y][x].append('')
            button = Button(background_normal = self.ball_color(color), on_press=self.move_object, size=self.size, border=(0,0,0,0))
            button.id = button_id
            self.grid[y][x] = Ball(ball, color, button, y, x)
            self.board_layout.add_widget(self.grid[y][x].button)
            counter += 1
        self.layout.add_widget(self.board_layout)

    # changing ball color
    def ball_color(self, number):
        colors = ('tile','aqua', 'black', 'blue', 
                'dark_green', 'light_green', 'orange', 'pink', 
                'red', 'yellow')
        color_list = {i: color for i, color in enumerate(colors)}

        color_ball = "resources/img/"+color_list[number]+".png"
        return color_ball

    # move the object
    def move_object(self, button):
        matching = button.id.split('-')
        row = int(matching[0])
        column = int(matching[1])
        ball = self.grid[row][column]
        if self.clicked == True:
            if row == self.prev_ball.row and column == self.prev_ball.column:
                self.reinit_prev()
                self.clicked = False
                print('movement aborted')
            elif row != self.prev_ball.row and column == self.prev_ball.column:
                if ball.color == '' and ball.number == 0:
                    self.place(row, column)
                    print(ball.color+' to '+str(row)+'-'+str(column))
            elif row == self.prev_ball.row and column != self.prev_ball.column:
                if ball.color == '' and ball.number == 0:
                    self.place(row, column)
                    print(ball.color+' to '+str(row)+'-'+str(column))
            else:
                print(ball.color+' invalid movement')
                return False
        else:
            if ball.color == self.turn:
                self.prev_ball = ball
                self.prev_color = ball.button.background_color
                ball.button.background_color = (0, 0.7, 0, 2)
                self.clicked = True
        return False 

    def place(self, row, column):
        if self.prev_ball.color == self.turn:
            self.check(row, column)
            return False
        return False

    # checking grid
    def check(self, row, column):
        if self.check_moveable(row, column) == True:
            if self.destroyed == False:
                self.change_turn()
        return False

    # moving check
    def check_moveable(self, row, column):
        if self.grid[row][column].color == '' and self.grid[row][column].number == 0:
            # if abs(row - self.prev_ball.row) == 2 and abs(column - self.prev_ball.column) == 2:
            #     if self.grid[int(row - ((row - self.prev_ball.row) / 2))][int(column - ((column - self.prev_ball.column) / 2))].color == self.players[self.turn].ennemy:
            #         self.grid[int(row - ((row - self.prev_ball.row) / 2))][int(column - ((column - self.prev_ball.column) / 2))].color = ''
            #         self.grid[int(row - ((row - self.prev_ball.row) / 2))][int(column - ((column - self.prev_ball.column) / 2))].button.text = ''
            #         self.update_score(self.players[self.turn].ennemy)
            #         self.pawnEated = True
            #         return self.swapPawnValues(row, column)
            # else:
            #     if row - self.prev_ball.row == self.players[self.turn].orientation and abs(column - self.prev_ball.column) == 1:
            #         return self.swapPawnValues(row, column)
            # for i in range (self.prev_ball.row+1, row):
            #     if row - self.prev_ball.row == i and abs(column - self.prev_ball.column) == 0:
            #         return self.swap_ball_values(row, column)  

            if abs(row - self.prev_ball.row) == 1 and column - self.prev_ball.column == 0:
                    return self.swap_ball_values(row, column)
            elif row - self.prev_ball.row == 0 and abs(column - self.prev_ball.column) == 1:
                    return self.swap_ball_values(row, column)
        return False

    def line_check(self, row, column):
        if (row + 1) < self.dynamic_value and (column + 1) < self.dynamic_value and  self.grid[row + 1][column + 1].color == self.players[self.turn]:
            if (row + 2) < self.dynamic_value and (column + 2) < self.dynamic_value and self.grid[row + 2][column + 2].color == '':
                return True
        if (row - 1) >= 0 and (column + 1) < self.dynamic_value and self.grid[row - 1][column + 1].color == self.players[self.turn]:
            if (row - 2) >= 0 and (column + 2) < self.dynamic_value and self.grid[row - 2][column + 2].color == '':
                return True
        if (row + 1) < self.dynamic_value and (column - 1) >= 0 and self.grid[row + 1][column - 1].color == self.players[self.turn]:
            if (row + 2) < self.dynamic_value and (column - 2) >= 0 and self.grid[row + 2][column - 2].color == '':
                return True
        if (row - 1) >= 0 and (column - 1) >= 0 and self.grid[row - 1][column - 1].color == self.players[self.turn]:
            if (row - 2) >= 0 and (column - 2) >= 0 and self.grid[row - 2][column - 2].color == '':
                return True
        return False       
    
    def reinit_prev(self):
        self.grid[self.prev_ball.row][self.prev_ball.column].button.background_color = self.prev_color
        self.grid[self.prev_ball.row][self.prev_ball.column].button.background_normal = self.ball_color(self.prev_ball.number)
        self.prev_ball = 0
    
    def swap_ball_values(self, row, column):
        self.grid[row][column].button.text, self.prev_ball.button.text = self.prev_ball.button.text, self.grid[row][column].button.text
        self.grid[row][column].color, self.prev_ball.color =  self.prev_ball.color, self.grid[row][column].color
        self.grid[row][column].number, self.prev_ball.number = self.prev_ball.number, self.grid[row][column].number
        if self.destroyed and self.line_check(row, column):
            self.grid[row][column].button.background_color = (0, 0.7, 0, 2)
            self.grid[self.prev_ball.row][self.prev_ball.column].button.background_color = self.prev_color
            self.prev_ball = self.grid[row][column]
            return True
        self.grid[row][column].button.background_normal = self.ball_color(self.grid[row][column].number)
        self.destroyed = False
        self.reinit_prev()
        return True

    def reinit_ball(self, ball):
        ball.color = ''
        ball.button.text = ''

    def change_turn(self):
        self.turn = self.players[self.turn].player
        self.count += 1
        print('turn '+str(self.count))
        self.clicked = False
        return False

    def restart(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.board_layout)

    def set_screen(self):
        # self.restart()
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
    active = BooleanProperty(False)
    sound = ObjectProperty(None, allownone=True)
    bgm_on = ObjectProperty(None)
    bgm_off = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SoundToggle, self).__init__(**kwargs)
        self.background_down = (0, 0, 1, 1)
        self.font_color_down = [1, 0, 0, 1]
        self.font_size = "12sp"
        self.allow_no_selection = False
        self.sound = BackgroundMusic()
        # self.bind(state = self.bgm_on_state)
        self.sfx = SoundEffects()

    def bgm_on_state(self, bgm, state):
        if self.bgm_on.state == 'down':
            self.bgm_off.state = 'normal'
            self.sound.play()
        elif self.bgm_off.state == 'down':
            self.bgm_on.state = 'normal'
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


if __name__ =="__main__":
    MainApp().run()