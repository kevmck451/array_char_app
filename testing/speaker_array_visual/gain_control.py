import customtkinter as ctk
import math


class SpeakerControlApp(ctk.CTk):
    def __init__(self, num_speakers=33, window_width=1450, window_height=950):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Enable dark mode
        ctk.set_default_color_theme("dark-blue")  # Optional: set a color theme

        self.title("Circular Speaker Array Control")
        self.num_speakers = num_speakers
        self.window_width = window_width
        self.window_height = window_height
        self.canvas_size = window_height - 350  # Adjust canvas size to fit within the window
        self.speaker_radius = 15
        self.speaker_positions = []
        self.gain_sliders = []
        self.slider_value_labels = []

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.create_widgets()
        self.draw_speaker_array()
        self.draw_mixer()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(self.main_frame, width=self.canvas_size, height=self.canvas_size, bg='#1e1e1e')
        self.canvas.pack(side=ctk.LEFT, padx=10, pady=10)

        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.global_control_frame = ctk.CTkFrame(self.control_frame)
        self.global_control_frame.pack(fill=ctk.X, pady=10)

        self.knob_label = ctk.CTkLabel(self.global_control_frame, text="Global Gain Level:")
        self.knob_label.pack(side=ctk.LEFT)

        self.knob = ctk.CTkSlider(self.global_control_frame, from_=0, to=100, orientation=ctk.HORIZONTAL, command=self.set_global_gain)
        self.knob.pack(side=ctk.LEFT, padx=5)
        self.knob.set(100)  # Default gain level

        self.set_all_zero_button = ctk.CTkButton(self.global_control_frame, text="Set All to 0", command=lambda: self.set_all_gains(0))
        self.set_all_zero_button.pack(side=ctk.LEFT, padx=5)

        self.set_all_max_button = ctk.CTkButton(self.global_control_frame, text="Set All to 100", command=lambda: self.set_all_gains(100))
        self.set_all_max_button.pack(side=ctk.LEFT, padx=5)

        self.update_button = ctk.CTkButton(self.global_control_frame, text="Update", command=self.update_visuals)
        self.update_button.pack(side=ctk.LEFT, padx=5)

        self.individual_control_frame = ctk.CTkFrame(self.control_frame)
        self.individual_control_frame.pack(fill=ctk.BOTH, expand=True)

        self.slider_frame = ctk.CTkFrame(self.individual_control_frame)
        self.slider_frame.pack()

    def draw_speaker_array(self):
        center_x, center_y = self.canvas_size // 2, self.canvas_size // 2
        radius = self.canvas_size // 2 - 20

        for i in range(self.num_speakers):
            angle = (2 * math.pi / self.num_speakers) * i - (math.pi / 2)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.speaker_positions.append((x, y))
            color = self.get_color_based_on_gain(100)  # Default color based on gain 100
            self.canvas.create_oval(x - self.speaker_radius, y - self.speaker_radius, x + self.speaker_radius, y + self.speaker_radius, fill=color, tags=f'speaker_{i}')
            self.canvas.create_text(x, y, text=str(i + 1), fill='white', tags=f'label_{i}')



    def draw_mixer(self):
        num_columns = 17  # Number of sliders per row
        for i in range(self.num_speakers):
            slider_frame = ctk.CTkFrame(self.slider_frame)
            slider_frame.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

            label = ctk.CTkLabel(slider_frame, text=f"S{i + 1}")
            label.pack()

            gain_slider = ctk.CTkSlider(slider_frame, from_=0, to=100, orientation=ctk.VERTICAL, height=100, command=lambda value, index=i: self.update_slider_value(value, index))
            gain_slider.set(100)  # Default gain level
            gain_slider.pack()

            slider_value_label = ctk.CTkLabel(slider_frame, text="100")  # Default value label
            slider_value_label.pack()

            self.gain_sliders.append(gain_slider)
            self.slider_value_labels.append(slider_value_label)

    def set_global_gain(self, value):
        for slider in self.gain_sliders:
            slider.set(int(value))
        for label in self.slider_value_labels:
            label.configure(text=str(int(value)))

    def set_all_gains(self, value):
        self.knob.set(value)
        self.set_global_gain(value)

    def update_visuals(self):
        for i, (x, y) in enumerate(self.speaker_positions):
            self.canvas.itemconfig(f'speaker_{i}', fill=self.get_color_based_on_gain(self.gain_sliders[i].get()))

    def update_slider_value(self, value, index):
        self.slider_value_labels[index].configure(text=str(int(value)))

    def get_color_based_on_gain(self, gain):
        # Function to change color based on gain level
        red_value = int(gain * 2.55)
        return f'#{red_value:02x}0000'

if __name__ == "__main__":
    app = SpeakerControlApp()
    app.mainloop()
