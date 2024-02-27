import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"





class App(customtkinter.CTk):
    def __init__(self, arm):
        super().__init__()
        self.arm=arm
        self.root = customtkinter.CTk()
        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="...", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Choisir photo", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Prendre photo", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        #self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        #self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        #self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        #self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand

        self.slider_button_minus = customtkinter.CTkButton(self.slider_progressbar_frame, text="-", command=self.decrement_slider)
        self.slider_button_minus.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="nsew")

        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=700,
                                                orientation="horizontal", command=self.sliding, height=10, width=500)
        self.slider_2.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky="ns")
        self.slider_2.set(300)

        self.slider_entry = customtkinter.CTkEntry(self.slider_progressbar_frame, width=50, justify="center")
        self.slider_entry.grid(row=1, column=2, padx=(10, 0), pady=(10, 10), sticky="nsew")
        self.slider_entry.insert(0, "300")
        self.slider_entry.bind("<Return>", self.set_slider_value)


        self.initial_position_button = customtkinter.CTkButton(self.slider_progressbar_frame, text="Position initiale", command=self.initial_position())
        self.initial_position_button.grid(row=2, column=1, padx=20, pady=10)


        self.slider_button_plus = customtkinter.CTkButton(self.slider_progressbar_frame, text="+", command=self.increment_slider)
        self.slider_button_plus.grid(row=1, column=3, padx=(0, 10), pady=10, sticky="nsew")


        # Create button x, y, z ... to control the robot
        self.control_position = customtkinter.CTkFrame(self, fg_color="transparent")
        self.control_position.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.control_position, text="...", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        #Les boutons x+, x-, y+, y-, z+, z- sont a placer ici
        self.control_position = customtkinter.CTkFrame(self, fg_color="transparent")

        self.control_position.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.control_position, text="...",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))

        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        # Add the buttons for controlling the robot's movement

        self.x_minus_button = customtkinter.CTkButton(self.control_position, text="x-",
                                                      command=lambda: self.move_robot("x", -1))

        self.x_minus_button.grid(row=1, column=0, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.x_plus_button = customtkinter.CTkButton(self.control_position, text="x+",
                                                     command=lambda: self.move_robot("x", 1))

        self.x_plus_button.grid(row=1, column=1, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.y_minus_button = customtkinter.CTkButton(self.control_position, text="y-",
                                                      command=lambda: self.move_robot("y", -1))

        self.y_minus_button.grid(row=2, column=0, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.y_plus_button = customtkinter.CTkButton(self.control_position, text="y+",
                                                     command=lambda: self.move_robot("y", 1))

        self.y_plus_button.grid(row=2, column=1, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.z_minus_button = customtkinter.CTkButton(self.control_position, text="z-",
                                                      command=lambda: self.move_robot("z", -1))

        self.z_minus_button.grid(row=3, column=0, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.z_plus_button = customtkinter.CTkButton(self.control_position, text="z+",
                                                     command=lambda: self.move_robot("z", 1))

        self.z_plus_button.grid(row=3, column=1, padx=(20, 0), pady=(10, 10), sticky="nsew")



        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.slider_2.configure()

        def move_robot(self, axis, direction):
            current_position = self.arm.position
            if axis == "x":
                target_position = [current_position[0] + direction, current_position[1], current_position[2]]
            elif axis == "y":
                target_position = [current_position[0], current_position[1] + direction, current_position[2]]
            elif axis == "z":
                target_position = [current_position[0], current_position[1], current_position[2] + direction]

            self.arm.set_position(x=target_position[0], y=target_position[1], z=target_position[2], speed=100,
                                  wait=True)



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def initial_position(self):
        pass

    def sliding(self, value):
        # update entry text
        value_int = int(value)
        self.slider_entry.delete(0, tkinter.END)
        self.slider_entry.insert(0, str(value_int))

    def set_slider_value(self, event):
        # get entry value and set slider value
        entry_value = self.slider_entry.get()
        if entry_value:
            self.slider_2.set(int(entry_value))

    def increment_slider(self):
        # increment slider value by 1
        current_value = self.slider_2.get()
        self.slider_2.set(current_value + 1)

    def decrement_slider(self):
        # decrement slider value by 1
        current_value = self.slider_2.get()
        self.slider_2.set(current_value - 1)

    def run(self):
        self.root.mainloop()
"""

if __name__ == "__main__":
    app = App()
    app.mainloop()"""