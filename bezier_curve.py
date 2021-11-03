from tkinter import Tk, Canvas, mainloop


from consts import HEIGHT, INTERVAL, WIDTH
from utils import random_color


class Bezier_Curve:
    window: Tk
    canvas: Canvas

    input_points = []

    t = 0
    points = []
    can_points = []
    can_lines = []

    arc = []

    p_last = ()
    color_last = ""

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Tkinter Animation Demo")
        self.window.geometry(f'{WIDTH}x{HEIGHT}')

        self.canvas = Canvas(self.window)
        self.canvas.configure(bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        self.animate()
        mainloop()


    def draw_point(self, p: tuple[int, int], radius: int = 5, color: str = "white"):
        return self.canvas.create_oval(p[0]-radius, p[1]-radius, p[0]+radius, p[1]+radius, fill=color)

    def redraw_point(self, id, p: tuple[int, int], radius: int = 5) -> None:
        self.canvas.coords(id, p[0]-radius, p[1]-radius, p[0]+radius, p[1]+radius)

    def draw_line(self, p0: tuple[int, int], p1: tuple[int, int], color: str = "white", width: int = 1):
        return self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], fill=color, width=width)

    def redraw_line(self, id, p0: tuple[int, int], p1: tuple[int, int]) -> None:
        self.canvas.coords(id, p0[0], p0[1], p1[0], p1[1])


    def get_point_on_line(self, p0: tuple[int, int], p1: tuple[int, int], t: float) -> tuple[int, int]:
        return (p0[0] + t * (p1[0]-p0[0]), p0[1] + t * (p1[1]-p0[1]))


    def left_click(self, event):
        self.input_points.append((event.x, event.y))
        self.reset()

    def right_click(self, event):
        self.input_points.pop()
        self.reset()


    def reset(self) -> None:
        if not len(self.input_points) > 0:
            return
        # remove old
        self.canvas.delete("all")
        # reset vars
        self.t = 0
        self.p_last = self.input_points[0]
        self.points = []
        self.can_points = []
        self.can_lines = []
        for i in range(len(self.input_points), 0, -1):
            self.points.append(self.input_points[:i])
                
        # create points
        for i in range(len(self.points)):
            self.color_last = random_color()
            d = []
            for p in self.points[i]:
                d.append(self.draw_point(p, color=self.color_last))
            self.can_points.append(d)

            d = []
            if len(self.points[i]) > 1:
                for j in range(len(self.points[i])-1):
                    d.append(self.draw_line(self.points[i][j], self.points[i][j+1], color=self.color_last))
            self.can_lines.append(d)


    def animate(self):
        self.t += INTERVAL
        if self.t >= 1:
            self.t = 0
            for id in self.arc:
                self.canvas.delete(id)
                self.p_last = self.points[0][0]

        if len(self.input_points) > 0:
            for i in range(1, len(self.points)):
                d = []
                for j in range(len(self.points[i])):
                    d.append(self.get_point_on_line(self.points[i-1][j], self.points[i-1][j+1], self.t))
                self.points[i] = d

                for j in range(len(self.points[i])):
                    self.redraw_point(self.can_points[i][j], self.points[i][j])

                if len(self.points[i]) > 1:
                    for j in range(len(self.points[i])-1):
                        self.redraw_line(self.can_lines[i][j], self.points[i][j], self.points[i][j+1])

            self.arc.append(self.draw_line(self.p_last, self.points[-1][0], color=self.color_last, width=2))
            self.p_last = self.points[-1][0]

        self.canvas.after(int(INTERVAL*1000), self.animate)
