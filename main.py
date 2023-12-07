import random
import pygame
import time


class Cell:
    def __init__(self, x, y, tile_size, options):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.options = options
        self.collapsed = False

    def entropy(self):
        return len(self.options)

    def observe(self):
        try:
            self.options = [random.choice(self.options)]
            self.collapsed = True
        except IndexError:
            return

    def draw(self, win):
        for i in range(len(self.options)):
            self.options[i].img.set_alpha(255//len(self.options))
            win.blit(self.options[i].img, (self.y *
                                           self.tile_size, self.x * self.tile_size))


class Tile:
    def __init__(self, img):
        self.img = img
        self.index = -1
        self.edges = []
        self.up, self.right, self.down, self.left = [], [], [], []

    def set_rules(self, tiles):
        for tile in tiles:
            self.check_relationships(tile.edges, tile)

    def check_relationships(self, other_edges, other_tile):
        for i in range(4):
            if self.edges[i] == other_edges[(i + 2) % 4]:
                getattr(self, ["up", "right", "down", "left"]
                        [i]).append(other_tile)


class Grid:
    def __init__(self, win, width, height, tile_size, options):
        self.win = win
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.w = self.width // self.tile_size
        self.h = self.height // self.tile_size
        self.grid = [[Cell(i, j, tile_size, options)
                      for j in range(self.h)] for i in range(self.w)]
        self.options = options
        self.invalid = False
        self.done = False

    def reset(self):
        self.grid = [[Cell(i, j, tile_size, self.options)
                      for j in range(self.h)] for i in range(self.w)]
        self.invalid = False
        print("reset")

    def heuristic_pick(self):
        print("heuristic pick")
        grid_copy = [i for row in self.grid for i in row]
        grid_copy.sort(key=lambda x: x.entropy())

        filtered_grid = [x for x in grid_copy if x.entropy() > 1]
        if not filtered_grid:
            print("done")
            print(self.grid[3][0].options[0].edges)
            self.done = True
            return None

        lowest_entropy = filtered_grid[0].entropy()
        filtered_grid = [
            x for x in filtered_grid if x.entropy() == lowest_entropy]

        pick = random.choice(filtered_grid)
        return pick

    def collapse(self):
        pick = self.heuristic_pick()
        if pick:
            self.grid[pick.x][pick.y].observe()
        else:
            return
        print(pick.x)
        print(pick.y)
        self.propagate(pick.x, pick.y)

    def propagate(self, i, j):
        time.sleep(.01)
        self.grid[i][j].draw(self.win)
        pygame.display.flip()
        pre_options = self.grid[i][j].options
        cumulative_valid_options = pre_options

        if len(pre_options) == 1:
            self.propagate_neighbor((i - 1, j))
            self.propagate_neighbor((i, j + 1))
            self.propagate_neighbor((i + 1, j))
            self.propagate_neighbor((i, j - 1))

        def check_neighbor_cell(cell, direction):
            neighbor = self.grid[cell[0] % self.w][cell[1] % self.h]
            valid_options = getattr(neighbor.options[0], direction, [])
            return [option for option in cumulative_valid_options if option in valid_options]

        cumulative_valid_options = check_neighbor_cell((i - 1, j), "down")
        cumulative_valid_options = check_neighbor_cell((i, j + 1), "left")
        cumulative_valid_options = check_neighbor_cell((i + 1, j), "up")
        cumulative_valid_options = check_neighbor_cell((i, j - 1), "right")

        if cumulative_valid_options:
            self.grid[i][j].options = cumulative_valid_options
            if len(cumulative_valid_options) == 1:
                self.grid[i][j].collapsed = True
            if pre_options != cumulative_valid_options:
                self.propagate_neighbor((i - 1, j))
                self.propagate_neighbor((i, j + 1))
                self.propagate_neighbor((i + 1, j))
                self.propagate_neighbor((i, j - 1))
        else:
            self.invalid = True

    def propagate_neighbor(self, cell):
        neighbor = self.grid[cell[0] % self.w][cell[1] % self.h]
        if not neighbor.collapsed:
            self.propagate(cell[0] % self.w, cell[1] % self.h)

    def draw(self, win):
        for row in self.grid:
            for cell in row:
                cell.draw(win)


pygame.init()

# Global variables
width = 600
height = 600
tile_size = 30
display = pygame.display.set_mode((width, height))


def load_image(path, tile_size_, padding=0):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(
        img, (tile_size_ - padding, tile_size_ - padding))
    return img


def main():
    options = [
        Tile(load_image(f"./imgs/{i}.png", tile_size)) for i in range(5)]

    options[0].edges = [0, 0, 0, 0]
    options[1].edges = [1, 1, 0, 1]
    options[2].edges = [1, 1, 1, 0]
    options[3].edges = [0, 1, 1, 1]
    options[4].edges = [1, 0, 1, 1]

    for i, tile in enumerate(options):
        tile.index = i
        tile.set_rules(options)

    wave = Grid(display, width, height, tile_size, options)
    display.fill((0, 0, 0))

    loop = True
    while loop:

        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loop = False

        wave.draw(display)
        if not wave.done:
            wave.collapse()
        if wave.invalid:
            wave.reset()
        pygame.display.flip()


if __name__ == "__main__":
    main()
