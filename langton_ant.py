import math
import pygame
import numpy as np

# The colors which will be used to color langston's universe
COLOR_LIST = {'RED':(255,0,0), 'GREEN':(0,255,0), 'GRAY':(211,211,211)}


class cube(object):
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def redraw(self, width, rows, surface):
        size = width // rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i*size + 1, j*size + 1, size-2, size-2))


class gameBoard(object):
    def __init__(self, width, rows, direction=0):
        """ Initializes the internal rep of the game board
            while also drawing the gameboard to the screen"""
        self.width = width
        self.rows = rows
        #direction is in set [0,1,2,3]
        self.direction = direction

        self.size_between = width // rows

        x = 0
        y = 0
        # first initialize the internal gameboard rep
        gameboard = []
        for i in range(rows**2):
            new_cube = cube(np.array([x,y]), COLOR_LIST['GRAY'])
            gameboard.append(new_cube)
            x += self.size_between
            #Test with i % rows == 0?
            if x % width == 0:
                x = 0
                y += self.size_between

        self.gameboard = np.asarray(gameboard)
        self.gameboard = self.gameboard.reshape(rows, rows)

        # the "ant" will be placed roughly in the center of the gameboard initially
        self.current_cube = self.gameboard[len(self.gameboard)//2, len(self.gameboard)//2]
        self.curr_cube_row = len(self.gameboard)//2
        self.curr_cube_col = len(self.gameboard)//2

        #now draw the game board
        self.win = pygame.display.set_mode((width, width))
        self.win.fill(COLOR_LIST['GRAY'])
        x = 0
        y = 0
        for l in range(self.rows):
            x += self.size_between
            y += self.size_between
            
            pygame.draw.line(self.win, (0,0,0), (x,0), (x,self.width))
            pygame.draw.line(self.win, (0,0,0), (0,y), (self.width,y))

    def update_current_cube(self):
        # first update color and direction
        if self.current_cube.color == COLOR_LIST['GRAY']:
            self.current_cube.color = COLOR_LIST['RED']
            self.direction = (self.direction - 1) % 4
        elif self.current_cube.color == COLOR_LIST['RED']:
            self.current_cube.color = COLOR_LIST['GRAY']
            self.direction = (self.direction + 1) % 4

        # Now move one "space" in the appropriate direction 
        if self.direction == 0:
            self.curr_cube_col -= 1
        elif self.direction == 1:
            self.curr_cube_row -= 1
        elif self.direction == 2:
            self.curr_cube_col += 1
        elif self.direction == 3:
            self.curr_cube_row += 1

        self.current_cube = self.gameboard[self.curr_cube_row, self.curr_cube_col]
        
    def redrawWindow(self):
        """Update the current cube color and all lines"""
        dist = self.size_between
        x = 0
        y = 0
        for l in range(self.rows):
            x += dist
            y += dist
            
            pygame.draw.line(self.win, (0,0,0), (x,0), (x,self.width))
            pygame.draw.line(self.win, (0,0,0), (0,y), (self.width,y))

        for r in range(self.rows):
            for c in range(self.rows):
                i = self.gameboard[r,c].position[0]
                j = self.gameboard[r,c].position[1]
                pygame.draw.rect(self.win, self.gameboard[r,c].color, (i*dist + 1, 
                    j*dist + 1, dist-2, dist-2))

        pygame.display.update()


if __name__ == '__main__':
    width = 500
    rows = 20
    ant_game = gameBoard(width, rows, 0)
    
    clock = pygame.time.Clock()

    i = 0
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        ant_game.update_current_cube()
        ant_game.redrawWindow()
        if i == 50:
            break
        i += 1