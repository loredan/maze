import colorsys
from matplotlib._cm import cubehelix as mcubehelix
import cubehelix

DIRECTIONS = ["LEFT", "TOP", "RIGHT", "BOTTOM"]


class Maze:

    def __init__(self, size):
        self.walls = []
        for i in range(size):
            column = []
            for j in range(size):
                column += [{DIRECTIONS[2]: False, DIRECTIONS[3]: False}]
            self.walls += [column]
        self.flood = self.Flood(self.walls, 0.01)
        self.colormap = mcubehelix()

    def set_wall(self, x, y, direction, wall):
        if x < 0 or y < 0 or x > len(self.walls) or y > len(self.walls) or x == len(
                self.walls) and direction == DIRECTIONS[2] or y == len(self.walls) and direction == DIRECTIONS[3]:
            return
        self.walls[x][y][direction] = wall

    def draw_flood(self, canvas, step_time_ms):
        flood_step = self.flood.step()
        # rgb = colorsys.hsv_to_rgb(flood_step["hue"] / 360, 1, 1)
        rgb = (self.colormap["red"](flood_step["position"]), self.colormap["green"](flood_step["position"]),
               self.colormap["blue"](flood_step["position"]))
        color = "#" + \
                str(hex(int(rgb[0] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[1] * 255)))[2:].rjust(2, '0') + \
                str(hex(int(rgb[2] * 255)))[2:].rjust(2, '0')
        for point in flood_step["front"]:
            canvas.create_rectangle(point["x"], point["y"], point["x"] + 1, point["y"] + 1, fill=color, width=0)
        if len(flood_step["front"]) > 0:
            canvas.after(step_time_ms, lambda: self.draw_flood(canvas, step_time_ms))

    class Flood:
        def __init__(self, walls, step):
            self.walls = walls
            self.position_step = step
            self.position = 0
            self.front = ({"x": 0, "y": 0, "from": DIRECTIONS[0]},)

        def get_wall(self, point, direction):
            wall_x = -1
            wall_y = -1
            wall_direction = ""
            if direction == DIRECTIONS[0]:
                wall_x = point["x"] - 1
                wall_y = point["y"]
                wall_direction = DIRECTIONS[2]
            elif direction == DIRECTIONS[1]:
                wall_x = point["x"]
                wall_y = point["y"] - 1
                wall_direction = DIRECTIONS[3]
            elif direction == DIRECTIONS[2]:
                wall_x = point["x"]
                wall_y = point["y"]
                wall_direction = DIRECTIONS[2]
            elif direction == DIRECTIONS[3]:
                wall_x = point["x"]
                wall_y = point["y"]
                wall_direction = DIRECTIONS[3]
            if wall_x < 0 or wall_y < 0 or wall_x > len(self.walls) or wall_y > len(self.walls) or \
                    wall_x == len(self.walls) - 1 and wall_direction == DIRECTIONS[2] or \
                    wall_y == len(self.walls) - 1 and wall_direction == DIRECTIONS[3]:
                return True
            return self.walls[wall_x][wall_y][wall_direction]

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

        def step_point(self, point):
            points = ()
            for direction in DIRECTIONS:
                if direction != point["from"] and not self.get_wall(point, direction):
                    points += (self.get_point(point, direction),)
            return points

        def step(self):
            new_front = ()
            for point in self.front:
                new_front += self.step_point(point)
            self.front = new_front
            self.position = (self.position + self.position_step) % 1
            return {"front": new_front, "position": self.position}
