import tkinter as tk
import math

class SpeakerControlApp(tk.Tk):
    def __init__(self, num_speakers=33, window_width=1450, window_height=950):
        super().__init__()
        self.title("Circular Speaker Array Control")
        self.num_speakers = num_speakers
        self.window_width = window_width
        self.window_height = window_height
        self.canvas_size = window_height - 350  # Adjust canvas size to fit within the window
        self.speaker_radius = 15
        self.speaker_positions = []
        self.gain_sliders = []

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.create_widgets()
        self.draw_speaker_array()

    def create_widgets(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.global_control_frame = tk.Frame(self.control_frame, bd=2, relief=tk.SUNKEN)
        self.global_control_frame.pack(fill=tk.X, pady=10)

        self.knob_label = tk.Label(self.global_control_frame, text="Global Gain Level:")
        self.knob_label.pack(side=tk.LEFT)

        self.knob = tk.Scale(self.global_control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_global_gain)
        self.knob.pack(side=tk.LEFT, padx=5)
        self.knob.set(100)  # Default gain level

        self.set_all_zero_button = tk.Button(self.global_control_frame, text="Set All to 0", command=lambda: self.set_all_gains(0))
        self.set_all_zero_button.pack(side=tk.LEFT, padx=5)

        self.set_all_max_button = tk.Button(self.global_control_frame, text="Set All to 100", command=lambda: self.set_all_gains(100))
        self.set_all_max_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(self.global_control_frame, text="Update", command=self.update_visuals)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.individual_control_frame = tk.Frame(self.control_frame, bd=2, relief=tk.SUNKEN)
        self.individual_control_frame.pack(fill=tk.BOTH, expand=True)

        self.slider_frame = tk.Frame(self.individual_control_frame)
        self.slider_frame.pack()

    def draw_speaker_array(self):
        center_x, center_y = self.canvas_size // 2, self.canvas_size // 2
        radius = self.canvas_size // 2 - 20

        for i in range(self.num_speakers):
            angle = (2 * math.pi / self.num_speakers) * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.speaker_positions.append((x, y))
            self.canvas.create_oval(x - self.speaker_radius, y - self.speaker_radius, x + self.speaker_radius, y + self.speaker_radius, fill='blue', tags=f'speaker_{i}')

        # Position sliders in rows of 6
        num_columns = 6  # Number of sliders per row
        for i in range(self.num_speakers):
            slider_frame = tk.Frame(self.slider_frame)
            slider_frame.grid(row=i // num_columns, column=i % num_columns, padx=5, pady=5)

            gain_slider = tk.Scale(slider_frame, from_=100, to=0, orient=tk.VERTICAL)
            gain_slider.set(100)  # Default gain level
            gain_slider.pack()

            label = tk.Label(slider_frame, text=f"Speaker {i+1}")
            label.pack()

            self.gain_sliders.append(gain_slider)

    def set_global_gain(self, value):
        for slider in self.gain_sliders:
            slider.set(int(value))

    def set_all_gains(self, value):
        self.knob.set(value)
        for slider in self.gain_sliders:
            slider.set(value)

    def update_visuals(self):
        for i, (x, y) in enumerate(self.speaker_positions):
            self.canvas.itemconfig(f'speaker_{i}', fill=self.get_color_based_on_gain(self.gain_sliders[i].get()))

    def get_color_based_on_gain(self, gain):
        # Example function to change color based on gain level
        return f'#{int(gain * 2.55):02x}00{int((100 - gain) * 2.55):02x}'

if __name__ == "__main__":
    app = SpeakerControlApp()
    app.mainloop()
