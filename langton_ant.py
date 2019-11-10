import pygame
import pygame.mixer
from pygame.locals import *

window_width = 1050
window_height = 600
window_dimension = (window_width, window_height)

DIVISIONS = 20

num_lines_width = window_width // DIVISIONS
num_lines_height = window_height // DIVISIONS

# 0 == "UP" 1 == "RIGHT" 2 == "DOWN" 3 == "LEFT"
direction = (0, 1, 2, 3)

COLOR_LIST = {"GREY": (150, 150, 150), "BLACK": (0, 0, 0), "WHITE": (255, 255, 255)}

window = pygame.display.set_mode(window_dimension)


def generate_lattice(lattice):
    color = (0, 0, 0)
    if lattice:
        color = COLOR_LIST["GREY"]
    else:
        color = COLOR_LIST["WHITE"]
    for i in range(0, window_width + 1, 1):
        if i % DIVISIONS == 0:
            pygame.draw.line(window, color, (i, 0), (i, window_height), 1)

    for i in range(0, window_height + 1, 1):
        if i % DIVISIONS == 0:
            pygame.draw.line(window, color, (0, i), (window_width, i), 1)


class Env:
    def __init__(self):
        self.gen = 0
        self.case = []
        self.orientation = direction[3]
        self.ant = [num_lines_height // 2, num_lines_width // 2]
        for i in range(num_lines_height):
            self.case.append([0] * num_lines_width)

    def is_out_of_bounds(self):
        if self.ant[0] >= num_lines_height or self.ant[1] >= num_lines_width:
            return True
        else:
            return False

    def update_orientation(self, dir):
        if dir == direction[1]:
            self.orientation = (self.orientation + 1) % 4
        elif dir == direction[3]:
            self.orientation = (self.orientation - 1) % 4

    def displace_ant(self):
        if self.orientation == direction[0]:
            self.ant[0] -= 1
        elif self.orientation == direction[2]:
            self.ant[0] += 1
        elif self.orientation == direction[1]:
            self.ant[1] += 1
        elif self.orientation == direction[3]:
            self.ant[1] -= 1

    def increment_gen(self):
        self.gen += 1

    def operation(self):
        if self.is_out_of_bounds():
            return False
        if self.case[self.ant[0]][self.ant[1]] == 0:
            self.update_orientation(direction[1])
            self.case[self.ant[0]][self.ant[1]] = 1
            pygame.draw.rect(window, COLOR_LIST["BLACK"],
                (self.ant[1]*DIVISIONS, self.ant[0]*DIVISIONS, DIVISIONS, DIVISIONS))
        else:
            self.update_orientation(direction[3])
            self.case[self.ant[0]][self.ant[1]] = 0
            pygame.draw.rect(window, COLOR_LIST["WHITE"], 
                (self.ant[1]*DIVISIONS, self.ant[0]*DIVISIONS, DIVISIONS, DIVISIONS))
        self.displace_ant()
        self.increment_gen()
        pygame.display.set_caption("Langton's Ant generation: " + str(self.gen))

        return True


if __name__ == '__main__':
    env = Env()
    window.fill(COLOR_LIST["WHITE"])
    pygame.init()

    timer = pygame.time.Clock()

    pygame.display.set_caption("Langton's Ant")

    lines = True
    finished = False

    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    finished = True
                if event.key == K_SPACE:
                    lines = False if lines else True

        timer.tick(5)
        
        generate_lattice(lines)
        if not env.operation() and end == 0:
            end = 1
            print("autoroute créée\nfin du programme")

        pygame.display.flip()
