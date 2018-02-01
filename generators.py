from maze import DIRECTIONS, Maze
import random


class RandomTraversal:

    def __init__(self) -> None:
        self.generated = [[0, 0]]
        self.front = [{"x": 0, "y": 0, "direction": DIRECTIONS[2]}, {"x": 0, "y": 0, "direction": DIRECTIONS[2]}]

    def generate(self, maze):
        counter = 0
        while len(self.front) > 0:
            self.step(maze)
            counter += 1
            if counter % 1000 == 0:
                print(counter, len(self.front))

    def step(self, maze):
        point = random.choice(self.front)
        self.front.remove(point)
        new_position = maze.get_point(point, point['direction'])
        new_position = [new_position['x'], new_position['y']]
        if 0 <= new_position[0] < len(maze.paths) and 0 <= new_position[1] < len(maze.paths) and \
                new_position not in self.generated:
            self.generated += [new_position]
            maze.set_path_point(point, True)
            for direction in DIRECTIONS:
                point = Maze.normalize_point(new_position[0], new_position[1], direction)
                if maze.get_path(point) == False:
                    self.front += [point]
