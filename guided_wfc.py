import copy
import random
import pygame
import random
import time

pygame.init()


class Cell:
    def __init__(self, x, y, rez, options):
        self.x = x
        self.y = y
        self.rez = rez
        self.options = options
        self.collapsed = False

    def draw(self, win):
        if len(self.options) == 1:
            win.blit(self.options[0].img, (self.y *
                                           self.rez, self.x * self.rez))

    # return the entropy/the length of options
    def entropy(self):
        return len(self.options)

    # update the collapsed variable
    def update(self):
        self.collapsed = bool(self.entropy() == 1)

    # observe the cell/collapse the cell
    def observe(self):
        try:
            self.options = [random.choice(self.options)]
            self.collapsed = True
        except:
            return


class Tile:
    def __init__(self, img):
        self.img = img
        self.index = -1
        self.edges = []
        self.up = []
        self.right = []
        self.down = []
        self.left = []

    # draw a single tile
    def draw(self, win, x, y):
        win.blit(self.img, (x, y))

    # set the rules for each tile
    def set_rules(self, tiles):
        for tile in tiles:
            # up
            if self.edges[0] == tile.edges[2]:
                self.up.append(tile)
            # right
            if self.edges[1] == tile.edges[3]:
                self.right.append(tile)
            # down
            if self.edges[2] == tile.edges[0]:
                self.down.append(tile)
            # left
            if self.edges[3] == tile.edges[1]:
                self.left.append(tile)

# Grid class


class Grid:
    def __init__(self, width, height, rez, options):
        self.width = width
        self.height = height
        self.rez = rez
        self.w = self.width // self.rez
        self.h = self.height // self.rez
        self.grid = []
        self.options = options

    # initiate each spot in the grid with a cell object
    def initiate(self):
        for i in range(self.w):
            self.grid.append([])
            for j in range(self.h):
                cell = Cell(i, j, self.rez, self.options)
                self.grid[i].append(cell)

    # draw each cell in the grid
    def draw(self, win):
        for row in self.grid:
            for cell in row:
                cell.draw(win)

    # randomly pick a cell using [entropy heuristic]
    def heuristic_pick(self):

        # shallow copy of a grid
        grid_copy = [i for row in self.grid for i in row]
        grid_copy.sort(key=lambda x: x.entropy())

        filtered_grid = list(filter(lambda x: x.entropy() > 1, grid_copy))
        if filtered_grid == []:
            return None

        initial = filtered_grid[0]
        filtered_grid = list(
            filter(lambda x: x.entropy() == initial.entropy(), filtered_grid))

        # return a pick if filtered copy os not empty
        pick = random.choice(filtered_grid)
        return pick

    # [WAVE FUNCTION COLLAPSE] algorithm
    def collapse(self):

        # pick a random cell using entropy heuristic
        pick = self.heuristic_pick()
        if pick:
            self.grid[pick.x][pick.y].options
            self.grid[pick.x][pick.y].observe()
        else:
            return

        # shallow copy of the gris
        next_grid = copy.copy(self.grid)

        # update the entropy values and superpositions of each cell in the grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j].collapsed:
                    next_grid[i][j] = self.grid[i][j]

                else:
                    # cumulative_valid_options will hold the options that will satisfy the "down", "right", "up", "left"
                    # conditions of each cell in the grid. The cumulative_valid_options is computed by,

                    cumulative_valid_options = self.options
                    # check above cell
                    cell_above = self.grid[(i - 1) % self.w][j]
                    # holds the valid options for the current cell to fit with the above cell
                    valid_options = []
                    for option in cell_above.options:
                        valid_options.extend(option.down)
                    cumulative_valid_options = [
                        option for option in cumulative_valid_options if option in valid_options]

                    # check right cell
                    cell_right = self.grid[i][(j + 1) % self.h]
                    # holds the valid options for the current cell to fit with the right cell
                    valid_options = []
                    for option in cell_right.options:
                        valid_options.extend(option.left)
                    cumulative_valid_options = [
                        option for option in cumulative_valid_options if option in valid_options]

                    # check down cell
                    cell_down = self.grid[(i + 1) % self.w][j]
                    # holds the valid options for the current cell to fit with the down cell
                    valid_options = []
                    for option in cell_down.options:
                        valid_options.extend(option.up)
                    cumulative_valid_options = [
                        option for option in cumulative_valid_options if option in valid_options]

                    # check left cell
                    cell_left = self.grid[i][(j - 1) % self.h]
                    # holds the valid options for the current cell to fit with the left cell
                    valid_options = []
                    for option in cell_left.options:
                        valid_options.extend(option.right)
                    cumulative_valid_options = [
                        option for option in cumulative_valid_options if option in valid_options]

                    # finally assign the cumulative_valid_options options to be the current cells valid options
                    # if len(cumulative_valid_options) == 0:
                    #     self.reset()
                    next_grid[i][j].options = cumulative_valid_options
                    next_grid[i][j].update()

        # re-assign the grid value after cell evaluation
        self.grid = copy.copy(next_grid)

    def reset(self):
        self.grid = []
        self.initiate()


# global variables
width = 600
height = 600
rez = 30
display = pygame.display.set_mode((width, height))


def load_image(path, rez_, padding=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (rez_ - padding, rez_ - padding))
    return img


def main():
    # loading tile images
    options = []
    for i in range(5):
        # load tetris tile
        img = load_image(f"./imgs/{i}.png", rez)

        options.append(Tile(img))

    options[0].edges = [0, 0, 0, 0]
    options[1].edges = [1, 1, 0, 1]
    options[2].edges = [1, 1, 1, 0]
    options[3].edges = [0, 1, 1, 1]
    options[4].edges = [1, 0, 1, 1]

    # update tile rules for each tile
    for i, tile in enumerate(options):
        tile.index = i
        tile.set_rules(options)

    # wave grid
    wave = Grid(width, height, rez, options)
    wave.initiate()

    # game loop
    loop = True
    while loop:
        time.sleep(.05)
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hover_toggle = not hover_toggle

                if event.key == pygame.K_q:
                    loop = False
                    exit()

        # grid draw function
        wave.draw(display)
        # grid collapse method to run the alogorithm
        wave.collapse()

        # update the display
        pygame.display.flip()

# --------------------------------------------------------------------------------- #


# calling the main function
if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------- #
