from abc import ABCMeta, abstractmethod, abstractproperty
import pygame
import pygame.gfxdraw as pydraw
import pygame.draw as pygdraw


class Grid():
    __metaclass__ = ABCMeta

    def __init__(self, parent, columns, rows, cell_size,
                 position, scale, color=(50, 50, 50)):

        self.cells = [[0 for i in range(columns)] for j in range(rows)]
        self.initial_size = cell_size
        self.scale = scale

        self.columns = columns
        self.rows = rows

        self.x, self.y = position

        self.last_moved = None

        self.parent = parent  # parent surface
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((206, 151, 219))
        self.surface.set_colorkey((0, 0, 0))

        self.grid_color = color

        self.filled = 0

        

    @abstractmethod
    def update_input(self, event):
        """ Updates input of user (zoom in/out, drag)"""
        pass

    @abstractmethod
    def update(self):
        """ Updates the state of grid """
        pass

    @abstractmethod
    def _check_winner(self, grid):
        """ Function that will compute the winner for certain grid """
        pass

    @abstractmethod
    def render(self):
        """ Renders grid surface, grid lines, cells """
        pass

    @abstractproperty
    def is_just_pressed(self):
        """ Returns False if not properly pressed, otherwise -> position"""
        pass

    def update_score(self):
        """ Updates score of each player """
        result = self._check_winner(self.cells)  
        if result == 0 and self.filled == self.columns * self.rows:
            return -2
        return result

    def convert(self, position):
        """ Converts absolute position to array position and returns False if unsuccessful"""
        x, y = position
        if not (self.x < x < self.x + self.width) or \
           not (self.y < y < self.y + self.height):

            return False

        return (self.grid_to_arr(self.surf_to_grid(position)))

    def add(self, value, position):
        """ Adds particular move to a position(relative to array), returns True if successful """

        if not self.cells[position[0]][position[1]]:
            self.cells[position[0]][position[1]] = value
            self.last_moved = position
            self.filled += 1
            return True
        else:
            return False

    def render_grid(self):
        """ Render lines and box of the grid """
        self.surface.fill((0, 0, 0))

        # Draws a box of grid
        pydraw.rectangle(self.surface, self.surface.get_rect(), (163, 39, 245))

        # Draws vertical lines
        for i in range(self.columns - 1):
            pydraw.vline(self.surface, (i+1)*self.cell_size, 0, self.height, self.grid_color)

        # Draws horizontal lines
        for j in range(self.rows - 1):
            pydraw.hline(self.surface, 0, self.width, (j+1)*self.cell_size, self.grid_color)

    def render_cells(self):
        # Renders all the cells acording to the content of the cell
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if self.cells[row][col] == 1:
                    self.render_cross((row, col))
                elif self.cells[row][col] == -1:
                    self.render_circle((row, col))

    def render_cross(self, position):
        """ Renders a cross at given position (relative to array) """
        # id = 1

        x, y = self.arr_to_grid(position)

        pygdraw.line(self.surface, (224, 74, 144),
                    (x, y),
                    (x + self.cell_size, y + self.cell_size), 12
                    )

        pygdraw.line(self.surface, (224, 74, 144),
                    (x + self.cell_size, y),
                    (x, y + self.cell_size), 12)

    def render_circle(self, position):
        """ Renders a circle at given position (relative to array) """
        # id = -1

        x, y = self.arr_to_grid(position)

        pygdraw.circle(self.surface, (134, 63, 181),
                        (x + self.cell_size//2, y + self.cell_size//2),
                        self.cell_size//2 - 1, 5)

        pygdraw.circle(self.surface, (134, 63, 181),
                        (x + self.cell_size//2, y + self.cell_size//2),
                        self.cell_size//4 - 1, 5)

    def grid_to_surf(self, pos):
        """ Converts Grid surface coordinates to Parent surface coordinates"""
        return (self.x + pos[0], self.y + pos[1])

    def surf_to_grid(self, pos):
        """ Converts Parent surface coordinates to Grid surface coordinates"""
        return (pos[0] - self.x, pos[1] - self.y)

    def arr_to_grid(self, pos):
        """ Converts Array coordinates to Grid surface coordinates"""
        return (pos[0] * self.cell_size, pos[1] * self.cell_size)

    def grid_to_arr(self, pos):
        """ Converts Grid surface coordinates to Array coordinates """
        return (pos[0] // self.cell_size, pos[1] // self.cell_size)

    def highlight(self, position):
        """ Highlights certain at position(relative to parent) """
        x, y = position

        if not (self.x < x < self.x + self.width) or \
           not (self.y < y < self.y + self.height):
            return
        x, y = self.surf_to_grid((x, y))
        x = (x // self.cell_size) * self.cell_size
        y = (y // self.cell_size) * self.cell_size
        x, y = self.grid_to_surf((x, y))
        # TODO: Change to surface related position
        pygame.draw.rect(self.parent, (220, 120, 245),
                         [x, y, self.cell_size, self.cell_size])

    @property
    def width(self):
        """ Current width of the grid """
        return self.cell_size * self.columns

    @property
    def height(self):
        """ Current height of the grid """
        return self.cell_size * self.rows

    @property
    def size(self):
        """ Current dimensions of the grid """
        return (self.width, self.height)

    @property
    def cell_size(self):
        """ Current scaled size of cells """
        return int(self.initial_size * self.scale)

    @property
    def position(self):
        return (self.x, self.y)
