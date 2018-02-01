from generators import RandomTraversal
from maze import *
from tkinter import *

root = Tk()
root.geometry("1000x1000+0+0")
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()
maze = Maze(100)
generator = RandomTraversal()
generator.generate(maze)
canvas.after(0, lambda: maze.draw_flood(canvas, 10))
root.mainloop()
