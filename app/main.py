from math import sqrt
from random import randint, sample

from core import Player, CheckerBall

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
    lines_ball = []
    free_cells = []
    set_balls = []
    next_balls = []
    selected = ''
    is_game_over = False
    destroyed = False
    prev_ball = ''
    prev_color = ''
    difficulty = ''
    layout = ''
    empty_cell = ''
    board_layout = ''
    turn = 'pl'
    count = 0
    clicked = False
    blocked = False
    loop_thread = None

    time_label = StringProperty()
    step_counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.coordinates = None
        self.set_balls = []
        self.event = Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.layout = self.ids.board_one
        self.dynamic_value = 10
        self.free_cells = []
        grid_value = self.dynamic_value * self.dynamic_value
        diviser = int(sqrt(grid_value))
        self.board_layout = GridLayout(cols = self.dynamic_value, rows = self.dynamic_value)
        nbBalls = int((self.dynamic_value / 2) * ((self.dynamic_value / 2 )- 1))
        self.players['pl'] = Player(name = 'Player', player = 'pl', score = nbBalls)
        counter = 0
        color = 0
        jumpline = 0
        random_balls = sample(range(0, grid_value), 3)
        ordering = sorted(random_balls)

        for i in range(0, grid_value):
            if jumpline != int(i/ diviser):
                jumpline += 1
                counter += 1

            try:
                value = self.grid[int(i / (diviser * (i % diviser)))]
            except Exception as e:
                self.grid.append([])

            button_id = str(int(i / diviser)) + '-' + str(int(i % diviser))

            y = int(i / diviser)
            x = int(i % diviser)

            self.grid[y].append([])
            self.grid[y][x].append('')
            self.free_cells.append((x, y))

            if i in ordering:
                ball = 'pl'
                color = randint(1, 9)
            else:
                ball = ''
                color = 0

            button = Button(on_press=self.move_object)
            button.id = button_id
            self.draw_tiles(button, color)
            self.grid[y][x] = CheckerBall(ball, color, button, y, x)
            if self.grid[y][x].ball == 'pl':
                self.free_cells.remove((x, y))
                self.set_balls.append((x, y))
            self.board_layout.add_widget(self.grid[y][x].button)
            counter += 1
        self.layout.add_widget(self.board_layout)

    def add_balls(self):
        for i in range(3):
            if len(self.free_cells) > 3:
                coord = self.free_cells[randint(0, len(self.free_cells)) - 1]
                self.grid[coord[1]][coord[0]].ball = 'pl'
                self.grid[coord[1]][coord[0]].color = randint(1, 9)
                self.grid[coord[1]][coord[0]].button.background_normal = self.ball_color(self.grid[coord[1]][coord[0]].color)
                self.free_cells.remove((coord[0], coord[1]))
            else:
                raise FieldFullException()

    def clear_board(self):
        self.free_cells.clear()
        for tile in range(0, int(self.dynamic_value * self.dynamic_value)):
            try:
                value = self.grid[int(tile / (self.dynamic_value * (tile % self.dynamic_value)))]
            except Exception as e:
                self.grid.append([])
            row = int(tile / self.dynamic_value)
            column = int(tile % self.dynamic_value)
            self.grid[row].append([])
            self.grid[row][column].append('')
            self.free_cells.append((row, column))

    def reset_board(self):
        self.clear_board()
        self.set_next_balls()

    #Finding line ball
    def find_lines(self, row, column):
        if self.grid[row][column].color == 0:
            return

        current_color = self.grid[row][column].color
        delete_ball = []

        minus_dx = column
        plus_dx = column + 1
        while minus_dx >= 0 and self.grid[row][minus_dx].color == current_color:
            delete_ball.append((minus_dx, row))
            minus_dx -= 1
        while plus_dx < self.dynamic_value and self.grid[row][plus_dx].color == current_color:
            delete_ball.append((plus_dx, row))
            plus_dx += 1
        if len(delete_ball) >= 5:
            return delete_ball
        else:
            delete_ball.clear()

        minus_dy = row
        plus_dy = row + 1
        while minus_dy >= 0 and self.grid[minus_dy][column].color == current_color:
            delete_ball.append((column, minus_dy))
            minus_dy -= 1
        while plus_dy < self.dynamic_value and self.grid[plus_dy][column].color == current_color:
            delete_ball.append((column, plus_dy))
            plus_dy += 1
        if len(delete_ball) >= 5:
            return delete_ball
        else:
            delete_ball.clear()

        minus_dx = column
        minus_dy = row
        plus_dx = column + 1
        plus_dy = row + 1
        while minus_dx >= 0 and minus_dy >= 0 and self.grid[minus_dy][minus_dx].color == current_color:
            delete_ball.append((minus_dx, minus_dy))
            minus_dx -= 1
            minus_dy -= 1
        while plus_dx < self.dynamic_value and plus_dy < self.dynamic_value and self.grid[plus_dy][plus_dx].color == current_color:
            delete_ball.append((plus_dx, plus_dy))
            plus_dx += 1
            plus_dy += 1
        if len(delete_ball) >= 5:
            return delete_ball
        else:
            delete_ball.clear()

        minus_dx = column
        plus_dy = row
        while minus_dx >= 0 and plus_dy < self.dynamic_value and self.grid[plus_dy][minus_dx].color == current_color:
            delete_ball.append((minus_dx, plus_dy))
            minus_dx -= 1
            plus_dy += 1

        plus_dx = column + 1
        minus_dy = row - 1
        while plus_dx < self.dynamic_value and minus_dy >= 0 and self.grid[minus_dy][plus_dx].color == current_color:
            delete_ball.append((plus_dx, minus_dy))
            plus_dx += 1
            minus_dy -= 1
        if len(delete_ball) >= 5:
            return delete_ball
        else:
            return

    #deleting line ball
    def delete_line(self, ball_coord_list):
        if ball_coord_list is not None:
            for coord in ball_coord_list:
                self.grid[coord[1]][coord[0]].ball = ''
                self.grid[coord[1]][coord[0]].color = 0
                self.grid[coord[1]][coord[0]].button.background_normal = self.ball_color(self.grid[coord[1]][coord[0]].color)
                self.free_cells.append((coord[0], coord[1]))

    # changing ball color
    def ball_color(self, color):
        colors = ('empty','aqua', 'black', 'blue',
                'dark_green', 'light_green', 'orange', 'pink',
                'red', 'yellow')
        color_list = {i: color for i, color in enumerate(colors)}

        color_ball = "resources/img/"+color_list[color]+".png"
        return color_ball

    #Drawing tiles
    def draw_tiles(self, button, color):
        button.background_normal = self.ball_color(color)
        button.size = self.size
        button.border = (0,0,0,0)

    #moving object using A* algorithm
    def moving(self, start_x, start_y, end_x, end_y):
        if (self.grid[end_y][end_x].ball != '' and self.grid[end_y][end_x].color != 0) or (self.grid[start_y][start_x].ball == '' and self.grid[start_y][start_x].color == 0):
            return False
        queue = []
        visited = []
        queue.append((start_x, start_y))
        while len(queue) != 0:
            coord = queue.pop(0)
            if coord[0] < 0 or coord[0] >= self.dynamic_value \
                or coord[1] < 0 or coord[1] >= self.dynamic_value:
                    continue
            if (coord != (start_x, start_y) and (self.grid[coord[1]][coord[0]].ball != '' and self.grid[coord[1]][coord[0]].color != 0)) \
                or (coord[0], coord[1]) in visited:
                    continue
            if coord[0] == end_x and coord[1] == end_y:
                return True
            visited.append((coord[0], coord[1]))
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 and dy != 0:
                        continue
                    else:
                        queue.append((coord[0] + dx, coord[1] + dy))
        return False

    # move the object
    def move_object(self, button):
        matching = button.id.split('-')
        row = int(matching[0])
        column = int(matching[1])
        ball = self.grid[row][column]

        if column < 0 or column >= self.dynamic_value or column < 0 or column >= self.dynamic_value:
            return

        if self.clicked == True:
            if row == self.prev_ball.row and column == self.prev_ball.column:
                self.reinit_prev()
                self.clicked = False
            elif ball.ball == '':
                if self.prev_ball.ball != '':
                    if self.moving(self.prev_ball.column, self.prev_ball.row, column, row):
                        self.place(self.prev_ball.row, self.prev_ball.column, row, column)
                        self.prev_ball = ''
                        find_lines = self.find_lines(row, column)
                        if find_lines is None:
                            self.add_balls()
                            for coordinates in self.set_balls:
                                array = self.find_lines(coordinates[0], coordinates[1])
                                if array is not None:
                                    self.delete_line(array)
                        else:
                            self.delete_line(find_lines)
            elif ball.ball != '':
                self.prev_ball = ball
                self.clicked = True
            else:
                return False
        else:
            if ball.ball == self.turn:
                self.prev_ball = ball
                self.clicked = True
        return False

    def place(self, prev_row, prev_column, row, column):
        if self.prev_ball.ball == self.turn:
            self.check(prev_row, prev_column, row, column)
            return False
        return False

    # checking grid
    def check(self, prev_row, prev_column, row, column):
        if self.check_moveable(prev_row, prev_column, row, column) == True:
            if self.destroyed == False:
                self.change_turn()
        return False

    # moving check
    def check_moveable(self, prev_row, prev_column, row, column):
        if self.grid[row][column].ball == '' and self.grid[row][column].color == 0:
            return self.swap_ball_values(prev_row, prev_column, row, column)
        return False

    # def update(self, *args):
    #     self.prev_ball

    def reinit_prev(self):
        self.grid[self.prev_ball.row][self.prev_ball.column].button.background_normal = self.ball_color(self.prev_ball.color)
        self.prev_ball = 0

    def swap_ball_values(self, prev_row, prev_column, row, column):
        self.grid[row][column].ball, self.grid[prev_row][prev_column].ball =  self.grid[prev_row][prev_column].ball, self.grid[row][column].ball
        self.grid[row][column].color, self.grid[prev_row][prev_column].color = self.grid[prev_row][prev_column].color, self.grid[row][column].color
        self.free_cells.remove((column, row))
        self.free_cells.append((prev_column, prev_row))
        self.grid[row][column].button.background_normal = self.ball_color(self.grid[row][column].color)
        self.destroyed = False
        self.reinit_prev()
        return True

    def change_turn(self):
        self.turn = self.players[self.turn].player
        self.count += 1
        self.clicked = False
        return False

    def game_over(self):
        self.is_game_over = True

    def restart(self):
        self.layout.clear_widgets()
        self.layout.add_widget(self.board_layout)

    def set_screen(self):
        MDApp.get_running_app().root.current = "start"
        MDApp.get_running_app().root.transition.direction = "right"

class FieldFullException(Exception):
    """Field full and no places to set next balls"""
    pass

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