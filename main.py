from maze import *
from tkinter import *

root = Tk()
root.geometry("500x500+0+0")
canvas = Canvas(root, width=500, height=500)
canvas.pack()
maze = Maze(500)
maze.walls = []
for i in range(500):
    column = []
    for j in range(500):
        column += [{DIRECTIONS[2]: j != 0, DIRECTIONS[3]: False}]
    maze.walls += [column]
maze.flood = maze.Flood(maze.walls, 0.01)
canvas.after(0, lambda: maze.draw_flood(canvas, 10))
root.mainloop()
