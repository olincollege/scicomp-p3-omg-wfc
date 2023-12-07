import copy
import random
import pygame

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
            self.options[0].draw(win, self.y * self.rez, self.x * self.rez)

    def entropy(self):
        return len(self.options)

    def update(self):
        self.collapsed = self.entropy() == 1

    def observe(self):
        try:
            self.options = [random.choice(self.options)]
            self.collapsed = True
        except IndexError:
            return


class Tile:
    def __init__(self, img):
        self.img = img
        self.index = -1
        self.edges = []
        self.up, self.right, self.down, self.left = [], [], [], []

    def draw(self, win, x, y):
        win.blit(self.img, (x, y))

    def set_rules(self, tiles):
        for tile in tiles:
            self.check_edge(tile.edges, tile)

    def check_edge(self, other_edges, other_tile):
        for i in range(4):
            if self.edges[i] == other_edges[(i + 2) % 4]:
                getattr(self, ["up", "right", "down", "left"]
                        [i]).append(other_tile)


class Grid:
    def __init__(self, width, height, rez, options):
        self.width = width
        self.height = height
        self.rez = rez
        self.w = self.width // self.rez
        self.h = self.height // self.rez
        self.grid = [[Cell(i, j, rez, options)
                      for j in range(self.h)] for i in range(self.w)]
        self.options = options

    def draw(self, win):
        for row in self.grid:
            for cell in row:
                cell.draw(win)

    def initiate(self):
        pass  # You might want to add implementation here if needed

    def heuristic_pick(self):
        grid_copy = [i for row in self.grid for i in row]
        grid_copy.sort(key=lambda x: x.entropy())

        filtered_grid = [x for x in grid_copy if x.entropy() > 1]
        if not filtered_grid:
            return None

        initial = filtered_grid[0]
        filtered_grid = [
            x for x in filtered_grid if x.entropy() == initial.entropy()]

        pick = random.choice(filtered_grid)
        return pick

    def collapse(self):
        pick = self.heuristic_pick()
        if pick:
            self.grid[pick.x][pick.y].observe()
        else:
            return

        next_grid = copy.deepcopy(self.grid)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j].collapsed:
                    next_grid[i][j] = self.grid[i][j]
                else:
                    self.compute_cumulative_valid_options(next_grid, i, j)

        self.grid = copy.deepcopy(next_grid)

    def compute_cumulative_valid_options(self, next_grid, i, j):
        cumulative_valid_options = self.options

        def check_neighbor_cell(cell, direction):
            neighbor = self.grid[cell[0] % self.w][cell[1] % self.h]
            valid_options = getattr(neighbor.options[0], direction, [])
            return [option for option in cumulative_valid_options if option in valid_options]

        cumulative_valid_options = check_neighbor_cell((i - 1, j), "down")
        cumulative_valid_options = check_neighbor_cell((i, j + 1), "left")
        cumulative_valid_options = check_neighbor_cell((i + 1, j), "up")
        cumulative_valid_options = check_neighbor_cell((i, j - 1), "right")

        next_grid[i][j].options = cumulative_valid_options
        next_grid[i][j].update()


# Global variables
width = 600
height = 600
rez = 30
display = pygame.display.set_mode((width, height))

hover_toggle = False  # Add missing variable initialization


def load_image(path, rez_, padding=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (rez_ - padding, rez_ - padding))
    return img


def main():
    options = [Tile(load_image(f"./imgs/{i}.png", rez)) for i in range(5)]

    for i, tile in enumerate(options):
        tile.index = i
        tile.set_rules(options)

    wave = Grid(width, height, rez, options)
    wave.initiate()

    loop = True
    while loop:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hover_toggle = not hover_toggle
                if event.key == pygame.K_q:
                    loop = False

        wave.draw(display)
        wave.collapse()
        pygame.display.flip()


if __name__ == "__main__":
    main()
