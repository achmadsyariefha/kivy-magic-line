# class BallColor:
#     type = ""
#     pictures = {
#         "ball_1":"resources/img/aqua.png",
#         "ball_2":"resources/img/black.png",
#         "ball_3":"resources/img/blue.png",
#         "ball_4":"resources/img/dark_green.png",
#         "ball_5":"resources/img/light_green.png",
#         "ball_6":"resources/img/orange.png",
#         "ball_7":"resources/img/pink.png",
#         "ball_8":"resources/img/red.png",
#         "ball_9":"resources/img/yellow.png"
#     }

#     def __init__(self, number):
#         self.number = number
#         self.subtype = self.get_subtype()
#         self.picture = self.pictures[self.subtype]

#     def get_subtype(self):
#         subtype = "_".join((self.type, self.number))
#         return subtype


#     def validate_moves(self, init_moves, colors):
#         removes = []
#         for move in init_moves:
#             if move not in colors.keys():
#                 removes.append(move)
#                 continue
#             color = colors[move]
#             if color.piece:
#                 removes.append(move)
#         moves = [m for m in init_moves if m not in removes]
#         return moves

#     def axis(self, coord, colors, direction):
#         moves = []
#         cell = coord
#         while True:
#             cell = (cell[0] + direction[0], cell[1] + direction[1])
#             if cell not in colors.keys():
#                 break
#             color = colors[cell]
#             if color.piece:
#                 moves.append(cell)
#             break
#         return moves
#     def axis_moves(self, coord, colors):
#         all_moves = []
#         for direction in self.directions:
#             moves = self.axis(coord, colors, direction)
#             all_moves.extend(moves)
#         return all_moves

# class Ball(BallColor):
#     type = "ball"

#     def get_moves(self, coord, colors):
#         init_moves = []
#         if self.coord[0] > 0 and self.coord[1] == 0:
#             move = (coord[0] - 1, coord[1])
#             move1 = (coord[0] + 1, coord[1])
#         elif self.coord[0] == 0 and self.coord[1] > 0:
#             move = (coord[0], coord[1]-1)
#             move1 = (coord[0], coord[1]+1)
#         else:
#             move = (coord[0] - 1, coord[1])
#             move1 = (coord[0] + 1, coord[1])
#             move2 = (coord[0], coord[1]-1)
#             move3 = (coord[0], coord[1]+1)
#         init_moves.append(move)
#         init_moves.append(move1)
#         init_moves.append(move2)
#         init_moves.append(move3)
#         moves = self.validate_moves(init_moves, colors)
#         return moves
class Ball:
    color = ''
    number = 0
    button = 0
    row = 0
    column = 0

    def __init__(self, color, number, button, row, column):
        self.color = color
        self.number = number
        self.button = button
        self.row = row
        self.column = column
        return

class Player:
    name = ''
    score = 0

    def __init__(self, name, player, score):
        self.name = name
        self.player = player
        self.score = score
        return
            

