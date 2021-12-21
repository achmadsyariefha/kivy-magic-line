class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end, allow_diagonal_movement = False):
    # start_node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    # end_node
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    #initialise both open and closed list
    open_list = []
    closed_list = []
    
    #add start node
    open_list.append(start_node)

    #which squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))
    #loop until you find the end
    while len(open_list) > 0:
        #get to current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        #pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        #found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] #return reversed path

        #generate children
        children = []
        for new_position in adjacent_squares: #adjacent squares
            #get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            #make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue
            #make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            #create new node
            new_node = Node(current_node, node_position)
            #append new noed
            children.append(new_node)

        #loop through children
        for child in children:
            #child is on closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            #create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            #child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            #add the child to the open list
            open_list.append(child)

def example():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)
