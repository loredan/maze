from tkinter import Canvas

import cubehelix

DIRECTIONS = ["LEFT", "TOP", "RIGHT", "BOTTOM"]


class Maze:

    def __init__(self, size):
        self.size = size
        self.paths = []
        self.reset_maze()
        self.flood = self.Flood(self, 10)
        self.colormap1 = cubehelix.cmap(startHue=-100, endHue=300, minLight=0.35, maxLight=0.8)
        self.colormap2 = cubehelix.cmap(startHue=540, endHue=140, minLight=0.35, maxLight=0.8, reverse=True)

    def reset_maze(self):
        self.paths = []
        for i in range(self.size):
            column = []
            for j in range(self.size):
                column += [{DIRECTIONS[2]: False if i < self.size - 1 else None,
                            DIRECTIONS[3]: False if j < self.size - 1 else None}]
            self.paths += [column]

    def set_path_point(self, point, path):
        self.set_path(point['x'], point['y'], point['direction'], path)

    def set_path(self, x, y, direction, path):
        if x < 0 or y < 0 or x > len(self.paths) or y > len(self.paths) or x == len(
                self.paths) and direction == DIRECTIONS[2] or y == len(self.paths) and direction == DIRECTIONS[3]:
            return
        self.paths[x][y][direction] = path

    def draw_maze(self, canvas: Canvas):
        scale = canvas.winfo_width() / (self.size * 2 + 1)
        canvas.create_rectangle(scale / 2, scale / 2, canvas.winfo_width() - scale / 2,
                                canvas.winfo_width() - scale / 2, width=scale)
        for i in range(self.size):
            for j in range(self.size):
                canvas.create_rectangle((i * 2 + 2) * scale, (j * 2 + 2) * scale, (i * 2 + 3) * scale,
                                        (j * 2 + 3) * scale, fill='black', width=0)
                if not self.paths[i][j][DIRECTIONS[2]]:
                    canvas.create_rectangle((i * 2 + 2) * scale, (j * 2 + 1) * scale, (i * 2 + 3) * scale,
                                            (j * 2 + 2) * scale, fill='black', width=0)
                if not self.paths[i][j][DIRECTIONS[3]]:
                    canvas.create_rectangle((i * 2 + 1) * scale, (j * 2 + 2) * scale, (i * 2 + 2) * scale,
                                            (j * 2 + 3) * scale, fill='black', width=0)

    def start_flood(self, canvas: Canvas, step_time_ms: int):
        self.flood.reset()
        self.draw_flood(canvas, step_time_ms)

    def draw_flood(self, canvas: Canvas, step_time_ms: int):
        scale = canvas.winfo_width() / (self.size * 2 + 1)
        flood_step = self.flood.step()
        rgb = self.to_rgba(flood_step["position"])
        color = "#" + \
                str(hex(int(rgb[0] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[1] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[2] * 255)))[2:].rjust(2, '0')
        for point in flood_step["front"]:
            canvas.create_rectangle((point["x"] * 2 + 1) * scale,
                                    (point["y"] * 2 + 1) * scale,
                                    (point["x"] * 2 + 2) * scale,
                                    (point["y"] * 2 + 2) * scale, fill=color, width=0)
            if point['from'] == DIRECTIONS[0]:
                canvas.create_rectangle((point["x"] * 2) * scale,
                                        (point["y"] * 2 + 1) * scale,
                                        (point["x"] * 2 + 1) * scale,
                                        (point["y"] * 2 + 2) * scale, fill=color, width=0)
            elif point['from'] == DIRECTIONS[1]:
                canvas.create_rectangle((point["x"] * 2 + 1) * scale,
                                        (point["y"] * 2) * scale,
                                        (point["x"] * 2 + 2) * scale,
                                        (point["y"] * 2 + 1) * scale, fill=color, width=0)
            elif point['from'] == DIRECTIONS[2]:
                canvas.create_rectangle((point["x"] * 2 + 2) * scale,
                                        (point["y"] * 2 + 1) * scale,
                                        (point["x"] * 2 + 3) * scale,
                                        (point["y"] * 2 + 2) * scale, fill=color, width=0)
            elif point['from'] == DIRECTIONS[3]:
                canvas.create_rectangle((point["x"] * 2 + 1) * scale,
                                        (point["y"] * 2 + 2) * scale,
                                        (point["x"] * 2 + 2) * scale,
                                        (point["y"] * 2 + 3) * scale, fill=color, width=0)
        if len(flood_step["front"]) > 0:
            canvas.after(step_time_ms, lambda: self.draw_flood(canvas, step_time_ms))

    def start_flood_terse(self, canvas, step_time_ms):
        self.flood.reset()
        self.draw_flood_terse(canvas, step_time_ms)

    def draw_flood_terse(self, canvas, step_time_ms):
        scale = canvas.winfo_width() / self.size
        flood_step = self.flood.step()
        rgb = self.to_rgba(flood_step["position"])
        color = "#" + \
                str(hex(int(rgb[0] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[1] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[2] * 255)))[2:].rjust(2, '0')
        for point in flood_step["front"]:
            canvas.create_rectangle(point["x"] * scale, point["y"] * scale, (point["x"] + 1) * scale,
                                    (point["y"] + 1) * scale, fill=color, width=0)
        if len(flood_step["front"]) > 0:
            canvas.after(step_time_ms, lambda: self.draw_flood_terse(canvas, step_time_ms))

    def to_rgba(self, value):
        if value < 256:
            return self.colormap1(value)
        else:
            return self.colormap2(value - 256)

    @staticmethod
    def normalize_point(x, y, direction):
        if direction == DIRECTIONS[0]:
            return {'x': x - 1, 'y': y, 'direction': DIRECTIONS[2]}
        elif direction == DIRECTIONS[1]:
            return {'x': x, 'y': y - 1, 'direction': DIRECTIONS[3]}
        elif direction == DIRECTIONS[2]:
            return {'x': x, 'y': y, 'direction': DIRECTIONS[2]}
        elif direction == DIRECTIONS[3]:
            return {'x': x, 'y': y, 'direction': DIRECTIONS[3]}

    def get_path(self, point):
        if point['x'] < 0 or point['y'] < 0 or point['x'] > len(self.paths) or point['y'] > len(self.paths):
            return None
        return self.paths[point['x']][point['y']][point['direction']]

    @staticmethod
    def get_point(point, direction):
        direction_from = DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]
        if direction == DIRECTIONS[0]:
            return {"x": point["x"] - 1, "y": point["y"], "from": direction_from}
        elif direction == DIRECTIONS[1]:
            return {"x": point["x"], "y": point["y"] - 1, "from": direction_from}
        elif direction == DIRECTIONS[2]:
            return {"x": point["x"] + 1, "y": point["y"], "from": direction_from}
        elif direction == DIRECTIONS[3]:
            return {"x": point["x"], "y": point["y"] + 1, "from": direction_from}

    class Flood:
        def __init__(self, maze, step):
            self.maze = maze
            self.position_step = step
            self.position = 0
            self.front = ()
            self.reset()

        def reset(self):
            self.position = 0
            self.front = ({"x": 0, "y": 0, "from": DIRECTIONS[0]},)

        def step_point(self, point):
            points = ()
            for direction in DIRECTIONS:
                if direction != point["from"] and self.maze.get_path(
                        Maze.normalize_point(point['x'], point['y'], direction)):
                    points += (Maze.get_point(point, direction),)
            return points

        def step(self):
            new_front = ()
            for point in self.front:
                new_front += self.step_point(point)
            self.front = new_front
            self.position = (self.position + self.position_step) % 512
            return {"front": new_front, "position": self.position}
