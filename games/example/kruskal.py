import random

# Easy to read representation for each cardinal direction.
N, S, W, E = ('n', 's', 'w', 'e')

class Cell(object):
    """
    Class for each individual cell. Knows only its position and which walls are
    still standing.
    """
    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)

    def __repr__(self):
        # <15, 25 (es  )>
        return '<{}, {} ({:4})>'.format(self.x, self.y, ''.join(sorted(self.walls)))

    def __contains__(self, item):
        # N in cell
        return item in self.walls

    def is_full(self):
        """
        Returns True if all walls are still standing.
        """
        return len(self.walls) == 4

    def _wall_to(self, other):
        """
        Returns the direction to the given cell from the current one.
        Must be one cell away only.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, '{}, {}'.format(self, other)
        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E
        else:
            assert False

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        other.walls.remove(other._wall_to(self))
        self.walls.remove(self._wall_to(other))

class Maze(object):
    """
    Maze class containing full board and maze generation algorithms.
    """

    def __init__(self, width=20, height=20):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.width = width
        self.height = height
        self.cells = []
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, E, W]))

    def __getitem__(self, index):
        """
        Returns the cell at index = (x, y).
        """
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells, not counting diagonals. Cells on
        borders or corners may have less than 4 neighbors.
        """
        x = cell.x
        y = cell.y
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[new_x, new_y]
            if neighbor is not None:
                yield neighbor

    def _gid_matrix(self):
        str_matrix = [[0] * (self.width * 2 + 1)
                      for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1
            str_matrix[y][x] = 1
            if N not in cell and y > 0:
                str_matrix[y - 1][x + 0] = 1
            if S not in cell and y + 1 < self.width:
                str_matrix[y + 1][x + 0] = 1
            if W not in cell and x > 0:
                str_matrix[y][x - 1] = 1
            if E not in cell and x + 1 < self.width:
                str_matrix[y][x + 1] = 1
        
        #print(str_matrix)
        
        data_list=[]
        
        for x in range(self.width*2+1):
            for y in range(self.height*2+1):
                data=0
                if str_matrix[x][y] == 1:
                    data = 57

                else:
                    data = 211 
                    if x == 0:
                        n = 1
                    else:
                        n = str_matrix[x-1][y]

                    if x == self.height*2:
                        s = 1
                    else:
                        s = str_matrix[x+1][y]

                    if y == 0:
                        w = 1
                    else:
                        w = str_matrix[x][y-1]

                    if y == self.width*2:
                        e = 1
                    else:
                        e = str_matrix[x][y+1]
                    print(n, e, s, w)

                    # append gid at array data
                    if n == 0 and e == 0 and s == 0 and w == 0:
                        data=241
                    elif n == 0 and e == 0 and s == 0 and w == 1:
                        data=225
                    elif n == 0 and e == 0 and s == 1 and w == 0:
                        data=239
                    elif n == 0 and e == 0 and s == 1 and w == 1:
                        data=223
                    elif n == 0 and e == 1 and s == 0 and w == 0:
                        data=233
                    elif n == 0 and e == 1 and s == 0 and w == 1:
                        data=217
                    elif n == 0 and e == 1 and s == 1 and w == 0:
                        data=231
                    elif n == 0 and e == 1 and s == 1 and w == 1:
                        data=215
                    elif n == 1 and e == 0 and s == 0 and w == 0:
                        data=237
                    elif n == 1 and e == 0 and s == 0 and w == 1:
                        data=221
                    elif n == 1 and e == 0 and s == 1 and w == 0:
                        data=235
                    elif n == 1 and e == 0 and s == 1 and w == 1:
                        data=219
                    elif n == 1 and e == 1 and s == 0 and w == 0:
                        data=229
                    elif n == 1 and e == 1 and s == 0 and w == 1:
                        data=213
                    elif n == 1 and e == 1 and s == 1 and w == 0:
                        data=227
                data_list.append(data)
        print(data_list)
        return data_list

    def randomize(self):
        """
        Knocks down random walls to build a random perfect maze.
        Algorithm from http://mazeworks.com/mazegen/mazetut/index.htm
        """
        cell_stack = []
        cell = random.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full()]
            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

    @staticmethod
    def generate(width=20, height=20):
        """
        Returns a new random perfect maze with the given sizes.
        """
        m = Maze(width, height)
        m.randomize()
        return m
                    

class MazeGame(object):
    """
    Class for interactively playing random maze games.
    """
    def __init__(self, maze):
        self.maze = maze or Maze.generate()

    def _get_random_position(self):
        """
        Returns a random position on the maze.
        """
        return (random.randrange(0, self.maze.width),
                random.randrange(0, self.maze.height))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        width = int(sys.argv[1])
        if len(sys.argv) > 2:
            height = int(sys.argv[2])
        else:
            height = width
    else:
        width = 20
        height = 20
    map_width = width*2+1
    map_height = height*2+1
    f = open("games/example/map1.tmx", 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?> \n')
    f.write('<map version="1.0" orientation="orthogonal" width="')
    f.write('%d" height="' % map_width)
    f.write('%d" tilewidth="64" tileheight="64"> \n' % map_height)
    f.write('<properties> \n')
    f.write('<property name="name" value="Blackrock"/> \n')
    f.write('</properties> \n')
    f.write('<tileset firstgid="1" name="graphics" tilewidth="64"   tileheight="64"> \n')
    f.write('<image source="graphics2x-basic.png" width="640"   height="1344"/> \n')
    f.write('</tileset> \n')
    f.write('<tileset firstgid="211" name="walls" tilewidth="64"    tileheight="64"> \n')
    f.write('<image source="graphics2x-walls.png" width="128"   height="1024"/> \n')
    f.write('</tileset> \n')
    f.write('<layer name="Tile Layer 1" width="%d" height="' % map_width)
    f.write('%d"> \n' % map_height)
    f.write('<data> \n')

    for i in Maze._gid_matrix(Maze.generate(width, height)):
        data = '<tile gid="%d"/>\n' % i
        f.write(data)
    f.write('</data> \n')
    f.write('</layer> \n')
    f.write('</map> \n')

    f.close()