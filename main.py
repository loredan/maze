from generators import RandomTraversal
from maze import *
from tkinter import *


class Controller:
    flooded = False

    def reset_display(self):
        self.flooded = False
        canvas.delete("all")
        if display_option.get() == 0:
            maze.draw_maze(canvas)

    def flood(self):
        if self.flooded:
            return
        self.flooded = True
        if display_option.get() == 0:
            canvas.after(0, lambda: maze.start_flood(canvas, 10))
        elif display_option.get() == 1:
            canvas.after(0, lambda: maze.start_flood_terse(canvas, 10))


root = Tk()
controller = Controller()

frame = Frame(root)
frame.pack(side=LEFT)

display_frame = LabelFrame(frame, text='Display')
display_frame.pack(side=TOP)

display_option = IntVar()
display_normal = Radiobutton(display_frame, text="Normal", variable=display_option, value=0,
                             command=controller.reset_display)
display_normal.pack(side=TOP)
display_terse = Radiobutton(display_frame, text="Terse", variable=display_option, value=1,
                            command=controller.reset_display)
display_terse.pack(side=TOP)
display_flood = Button(display_frame, text="Flood", command=controller.flood)
display_flood.pack(side=TOP)

canvas = Canvas(root, width=1000, height=1000)
canvas.pack(side=RIGHT)

root.update()

maze = Maze(200)
generator = RandomTraversal()
generator.generate(maze)
display_normal.select()
root.mainloop()
