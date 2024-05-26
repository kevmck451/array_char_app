import customtkinter as ctk
import math
from tkinter import filedialog, StringVar, Listbox, Scrollbar, END, SINGLE
from pathlib import Path

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
        self.file_list = [
            "/path/to/sound1.wav",
            "/path/to/sound2.wav",
            "/path/to/sound3.wav"
        ]
        self.playing = False
        self.selected_file = StringVar()

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.create_widgets()
        self.draw_speaker_array()
        self.draw_mixer()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)

        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ctk.CTkFrame(self.top_frame)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)

        self.file_listbox_frame = ctk.CTkFrame(self.left_frame)
        self.file_listbox_frame.pack(fill=ctk.Y, expand=False, pady=(0, 5))

        self.file_listbox = Listbox(self.file_listbox_frame, selectmode=SINGLE, height=6)
        self.file_listbox.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.scrollbar = Scrollbar(self.file_listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.file_listbox.yview)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        for file in self.file_list:
            self.file_listbox.insert(END, Path(file).stem)

        self.load_file_button = ctk.CTkButton(self.left_frame, text="Load File", command=self.load_file)
        self.load_file_button.pack(pady=5)

        self.play_button = ctk.CTkButton(self.left_frame, text="Play", fg_color="green", command=self.toggle_play)
        self.play_button.pack(pady=5)

        self.sequence_frame = ctk.CTkFrame(self.left_frame)
        self.sequence_frame.pack(pady=5)

        self.sequence_1_button = ctk.CTkButton(self.sequence_frame, text="Sequence 1")
        self.sequence_1_button.pack(side=ctk.LEFT, padx=5)

        self.sequence_2_button = ctk.CTkButton(self.sequence_frame, text="Sequence 2")
        self.sequence_2_button.pack(side=ctk.LEFT, padx=5)

        self.canvas_frame = ctk.CTkFrame(self.top_frame)
        self.canvas_frame.pack(side=ctk.LEFT, expand=True)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size, bg='#1e1e1e')
        self.canvas.pack(expand=True, padx=10, pady=10)

        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        self.global_control_frame = ctk.CTkFrame(self.bottom_frame)
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

        self.slider_frame = ctk.CTkFrame(self.bottom_frame)
        self.slider_frame.pack(fill=ctk.X, padx=5, pady=5)  # Ensure the sliders take up the full width

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.file_list.append(file_path)
            self.file_listbox.insert(END, Path(file_path).stem)

    def toggle_play(self):
        if self.playing:
            self.play_button.configure(text="Play", fg_color="green")
            self.playing = False
            # Placeholder for stopping audio
        else:
            self.play_button.configure(text="Stop", fg_color="red")
            self.playing = True
            # Placeholder for playing audio

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
        for i in range(self.num_speakers):
            slider_frame = ctk.CTkFrame(self.slider_frame)
            slider_frame.pack(side=ctk.LEFT, padx=5, pady=5)

            if i < 10:
                label = ctk.CTkLabel(slider_frame, text=f"S0{i + 1}")
            else:
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
