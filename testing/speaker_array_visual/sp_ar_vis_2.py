import tkinter as tk
import math


class SpeakerControlApp(tk.Tk):
    def __init__(self, num_speakers=33):
        super().__init__()
        self.title("Circular Speaker Array Control")
        self.num_speakers = num_speakers
        self.canvas_size = 800  # Increased canvas size to better fit sliders
        self.speaker_radius = 10
        self.speaker_positions = []
        self.gain_sliders = []

        self.create_widgets()
        self.draw_speaker_array()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        self.control_frame = tk.Frame(self)
        self.control_frame.pack()

        self.knob_label = tk.Label(self.control_frame, text="Control Knob (Gain Level):")
        self.knob_label.pack(side=tk.LEFT)

        self.knob = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.knob.pack(side=tk.LEFT)
        self.knob.set(100)  # Default gain level

        self.update_button = tk.Button(self.control_frame, text="Update", command=self.update_visuals)
        self.update_button.pack(side=tk.LEFT)

    def draw_speaker_array(self):
        center_x, center_y = self.canvas_size // 2, self.canvas_size // 2
        radius = self.canvas_size // 2 - 60  # Adjusted radius to fit sliders

        for i in range(self.num_speakers):
            angle = (2 * math.pi / self.num_speakers) * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.speaker_positions.append((x, y))
            self.canvas.create_oval(x - self.speaker_radius, y - self.speaker_radius, x + self.speaker_radius, y + self.speaker_radius, fill='blue', tags=f'speaker_{i}')

            # Position sliders around the circle
            slider_x = center_x + (radius + 40) * math.cos(angle)
            slider_y = center_y + (radius + 40) * math.sin(angle)
            slider = tk.Scale(self, from_=100, to=0, orient=tk.VERTICAL)
            slider.set(100)  # Default gain level
            slider.place(x=slider_x, y=slider_y, anchor=tk.CENTER)
            self.gain_sliders.append(slider)

            # Add labels to sliders
            label = tk.Label(self, text=f"Speaker {i+1}")
            label.place(x=slider_x, y=slider_y + 60, anchor=tk.CENTER)

    def update_visuals(self):
        for i, (x, y) in enumerate(self.speaker_positions):
            self.canvas.itemconfig(f'speaker_{i}', fill=self.get_color_based_on_gain(self.gain_sliders[i].get()))

    def get_color_based_on_gain(self, gain):
        # Example function to change color based on gain level
        return f'#{int(gain * 2.55):02x}00{int((100 - gain) * 2.55):02x}'


if __name__ == "__main__":
    app = SpeakerControlApp()
    app.mainloop()
