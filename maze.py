import cubehelix

DIRECTIONS = ["LEFT", "TOP", "RIGHT", "BOTTOM"]


class Maze:

    def __init__(self, size):
        self.size = size
        self.paths = []
        for i in range(size):
            column = []
            for j in range(size):
                column += [
                    {DIRECTIONS[2]: False if i < size - 1 else None, DIRECTIONS[3]: False if j < size - 1 else None}]
            self.paths += [column]
        self.flood = self.Flood(self, 10)
        self.colormap1 = cubehelix.cmap(startHue=-100, endHue=300, minLight=0.35, maxLight=0.8)
        self.colormap2 = cubehelix.cmap(startHue=540, endHue=140, minLight=0.35, maxLight=0.8, reverse=True)

    def set_path_point(self, point, path):
        self.set_path(point['x'], point['y'], point['direction'], path)

    def set_path(self, x, y, direction, path):
        if x < 0 or y < 0 or x > len(self.paths) or y > len(self.paths) or x == len(
                self.paths) and direction == DIRECTIONS[2] or y == len(self.paths) and direction == DIRECTIONS[3]:
            return
        self.paths[x][y][direction] = path

    def draw_flood(self, canvas, step_time_ms):
        flood_step = self.flood.step()
        scale = canvas.winfo_width() / self.size
        # rgb = colorsys.hsv_to_rgb(flood_step["hue"] / 360, 1, 1)
        rgb = self.to_rgba(flood_step["position"])
        color = "#" + \
                str(hex(int(rgb[0] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[1] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[2] * 255)))[2:].rjust(2, '0')
        for point in flood_step["front"]:
            canvas.create_rectangle(point["x"] * scale, point["y"] * scale, (point["x"] + 1) * scale,
                                    (point["y"] + 1) * scale, fill=color, width=0)
        if len(flood_step["front"]) > 0:
            canvas.after(step_time_ms, lambda: self.draw_flood(canvas, step_time_ms))

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
