import tkinter as tk
from functools import partial

class RobotControlApp:
    def __init__(self, arm):
        self.arm = arm
        self.root = tk.Tk()
        self.root.title("Robot Control Interface")

        self.move_buttons = {
            "x+": partial(self.move_axis, "x", 1),
            "x-": partial(self.move_axis, "x", -1),
            "y+": partial(self.move_axis, "y", 1),
            "y-": partial(self.move_axis, "y", -1),
            "z+": partial(self.move_axis, "z", 1),
            "z-": partial(self.move_axis, "z", -1),
        }

        for button_text, command in self.move_buttons.items():
            btn = tk.Button(self.root, text=button_text, command=command)
            btn.pack()

    def move_axis(self, axis, direction):
        current_position = self.arm.position
        if axis == "x":
            target_position = [current_position[0] + direction, current_position[1], current_position[2]]
        elif axis == "y":
            target_position = [current_position[0], current_position[1] + direction, current_position[2]]
        elif axis == "z":
            target_position = [current_position[0], current_position[1], current_position[2] + direction]

        self.arm.set_position(x=target_position[0], y=target_position[1], z=target_position[2], speed=100, wait=True)

    def run(self):
        self.root.mainloop()