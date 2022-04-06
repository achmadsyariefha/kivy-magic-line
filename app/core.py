
from random import randint

class CheckerBall:

    def __init__(self, ball = '', color = 0, button = 0, row = 0, column = 0):
        self.ball = ball
        self.color = color
        self.button = button
        self.row = row
        self.column = column
        self.clicked = False
        return

    def __eq__(self, other):
        """Define the equality of balls"""
        return self.color == other.color

    def set_color(self, color):
        """Set the color (number) of the ball"""
        self.color = color

    def set_random_color(self, number_of_colors):
        """Determine the color of the ball"""
        self.color = randint(1, number_of_colors)

class Player:
    name = ''
    score = 0

    def __init__(self, name, player, score):
        self.name = name
        self.player = player
        self.score = score
        return



