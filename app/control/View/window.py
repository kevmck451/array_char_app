import app.control.View.window_con as window_con
from app.control.Controller.events import Event
from app.docs.resources import base_path

import customtkinter as ctk
import math
from tkinter import filedialog, StringVar, Listbox, Scrollbar, END, SINGLE
from pathlib import Path
import tkinter as tk


class SpeakerControlApp(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Enable dark mode
        ctk.set_default_color_theme("dark-blue")  # Optional: set a color theme

        self.title(window_con.window_title)
        self.event_handler = event_handler

        self.window_width = window_con.window_width
        self.window_height = window_con.window_height

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_con.window_width / 2))
        center_y = int((screen_height / 2) - (window_con.window_height / 2))
        self.geometry(f'{window_con.window_width}x{window_con.window_height}+{center_x}+{center_y}')
        self.minsize(window_con.min_window_width, window_con.min_window_height)

        self.num_speakers = 36
        self.canvas_size = window_con.speaker_array_canvas_size
        self.speaker_radius = window_con.speaker_radius
        self.speaker_positions = []
        self.gain_sliders = []
        self.slider_value_labels = []
        self.playing = False
        self.hardware_state = 0
        self.selected_file = StringVar()
        self.real_time_update = False
        self.load_box_limit = 8
        self.current_file_selection = None

        audio_filepath = base_path('audio_files')
        self.file_list = [x for x in Path(audio_filepath).iterdir()]

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.create_widgets()
        self.draw_speaker_array()
        self.draw_mixer()

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)

        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ctk.CTkFrame(self.top_frame)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=10, pady=10)

        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        self.global_control_frame = ctk.CTkFrame(self.bottom_frame)
        self.global_control_frame.pack(fill=ctk.X, pady=10)

        # -----------------------------------------------------------------------------------
        # HARDWARE CONNECTION FRAME --------------
        # -----------------------------------------------------------------------------------
        underline_font = ctk.CTkFont(family="default_font", size=30, underline=True)
        hardware_connect = ctk.CTkLabel(self.left_frame, text='Hardware Connection', font=underline_font)
        hardware_connect.pack(pady=30)

        self.hardware_connect_button = ctk.CTkButton(self.left_frame, text="Connect",
                                                     fg_color=window_con.start_fg_color,
                                                     hover_color=window_con.start_hover_color,
                                                     command=lambda: self.event_handler(Event.CONNECT_HARDWARE))
        self.hardware_connect_button.pack()

        # -----------------------------------------------------------------------------------
        # MEDIA SELECT FRAME --------------
        # -----------------------------------------------------------------------------------

        media_select_title = ctk.CTkLabel(self.left_frame, text='Media Select Options', font=underline_font)
        media_select_title.pack(pady=30)

        self.file_listbox_frame = ctk.CTkFrame(self.left_frame)
        self.file_listbox_frame.pack(fill=ctk.Y, expand=False, pady=(0, 5))

        self.file_listbox = Listbox(self.file_listbox_frame, selectmode=SINGLE, height=self.load_box_limit)
        self.file_listbox.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.scrollbar = Scrollbar(self.file_listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.file_listbox.yview)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        for file in self.file_list:
            self.file_listbox.insert(END, Path(file).stem)

        # Bind the selection event
        self.file_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.load_file_button = ctk.CTkButton(self.left_frame, text="Load File", command=self.load_file)
        self.load_file_button.pack(pady=5)

        # -----------------------------------------------------------------------------------
        # PLAYBACK FRAME --------------
        # -----------------------------------------------------------------------------------

        playback_options = ctk.CTkLabel(self.left_frame, text='Playback Options', font=underline_font)
        playback_options.pack(pady=30)

        self.play_button = ctk.CTkButton(self.left_frame, text="Play",
                                         fg_color=window_con.start_fg_color,
                                         hover_color=window_con.start_hover_color,
                                         command = self.play_audio)
        self.play_button.pack(pady=5)

        self.sequence_frame = ctk.CTkFrame(self.left_frame)
        self.sequence_frame.pack(pady=5)

        self.sequence_1_button = ctk.CTkButton(self.sequence_frame, text="Sequence 1",
                                               fg_color=window_con.reset_fg_color,
                                               hover_color=window_con.reset_hover_color)

        self.sequence_1_button.pack(side=ctk.LEFT, padx=5)

        self.sequence_2_button = ctk.CTkButton(self.sequence_frame, text="Sequence 2",
                                               fg_color=window_con.reset_fg_color,
                                               hover_color=window_con.reset_hover_color)

        self.sequence_2_button.pack(side=ctk.LEFT, padx=5)

        # -----------------------------------------------------------------------------------
        # SPEAKER ARRAY FRAME --------------
        # -----------------------------------------------------------------------------------

        self.canvas_frame = ctk.CTkFrame(self.top_frame)
        self.canvas_frame.pack(side=ctk.LEFT, expand=True)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size, bg='#1e1e1e')
        self.canvas.pack(expand=True, padx=10, pady=10)

        # -----------------------------------------------------------------------------------
        # MIXER FRAME --------------
        # -----------------------------------------------------------------------------------

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

        self.real_time_button = ctk.CTkButton(self.global_control_frame, text="Real Time", fg_color="gray", command=self.toggle_real_time)
        self.real_time_button.pack(side=ctk.LEFT, padx=5)

        self.slider_frame = ctk.CTkFrame(self.bottom_frame)
        self.slider_frame.pack(fill=ctk.X, padx=5, pady=5)  # Ensure the sliders take up the full width

    def on_listbox_select(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            self.current_file_selection = self.file_listbox.get(selected_index)

    def toggle_hardware_connect(self):
        if self.hardware_state == 0:
            self.hardware_connect_button.configure(text="Attempting...",
                                                   fg_color=window_con.pause_fg_color,
                                                   hover_color=window_con.pause_hover_color,
                                                   command=lambda: self.event_handler(Event.DISCONNECT_HARDWARE))
        elif self.hardware_state == 1:
            self.hardware_connect_button.configure(text="Disconnect Hardware",
                                                   fg_color=window_con.stop_fg_color,
                                                   hover_color=window_con.stop_hover_color,
                                                   command=lambda: self.event_handler(Event.DISCONNECT_HARDWARE))
        else:
            self.hardware_connect_button.configure(text="Connect Hardware",
                                                   fg_color=window_con.start_fg_color,
                                                   hover_color=window_con.start_hover_color,
                                                   command=lambda: self.event_handler(Event.CONNECT_HARDWARE))

    def toggle_real_time(self):
        self.real_time_update = not self.real_time_update
        if self.real_time_update:
            self.real_time_button.configure(fg_color="blue")
        else:
            self.real_time_button.configure(fg_color="gray")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.file_list.append(file_path)
            self.file_listbox.insert(END, Path(file_path).stem)

    def toggle_play(self):
        if self.playing:
            self.play_button.configure(text="Play",
                                       fg_color=window_con.start_fg_color,
                                       hover_color=window_con.start_hover_color,
                                       command=self.play_audio)
            self.playing = False
            # Placeholder for stopping audio
        else:
            self.play_button.configure(text="Stop",
                                       fg_color=window_con.stop_fg_color,
                                       hover_color=window_con.stop_hover_color,
                                       command=lambda: self.event_handler(Event.STOP_AUDIO))
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
            color = self.get_color_based_on_gain(0)  # Default color based on gain 100
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
            gain_slider.set(0)  # Default gain level
            gain_slider.pack()

            slider_value_label = ctk.CTkLabel(slider_frame, text="0")  # Default value label
            slider_value_label.pack()

            self.gain_sliders.append(gain_slider)
            self.slider_value_labels.append(slider_value_label)

    def set_global_gain(self, value):
        for slider in self.gain_sliders:
            slider.set(int(value))
        for label in self.slider_value_labels:
            label.configure(text=str(int(value)))
        if self.real_time_update:
            self.update_visuals()

    def set_all_gains(self, value):
        self.knob.set(value)
        self.set_global_gain(value)

    def update_visuals(self):
        for i, (x, y) in enumerate(self.speaker_positions):
            self.canvas.itemconfig(f'speaker_{i}', fill=self.get_color_based_on_gain(self.gain_sliders[i].get()))

    def update_slider_value(self, value, index):
        self.slider_value_labels[index].configure(text=str(int(value)))
        if self.real_time_update:
            self.update_visuals()

    def get_color_based_on_gain(self, gain):
        # Function to change color based on gain level
        red_value = int(gain * 2.55)
        return f'#{red_value:02x}0000'

    def play_audio(self):
        if self.current_file_selection is not None:
            self.event_handler(Event.PLAY_AUDIO)
        else:
            self.warning_popup_general('Select Audio from List')
            # print('Select Audio from List')

    def warning_popup_general(self, message):
        message_popup = tk.Toplevel(self)
        message_popup.title("Message")
        window_width = 400
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        message_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Display the message
        tk.Label(message_popup, text=message, font=("default_font", 16)).pack(pady=20)

        # OK button to close the pop-up
        ok_button = tk.Button(message_popup, text="OK", background="#D3D3D3", padx=10, pady=10,
                              command=message_popup.destroy)
        ok_button.pack(pady=10)

    def on_close(self):
        # print('x button pressed')
        self.event_handler(Event.ON_CLOSE)
        self.destroy()