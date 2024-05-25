import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

import app.hardware.View.configuration as configuration
from app.hardware.Controller.events import Event


class Main_Window(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.event_handler = event_handler

        # Main Setup ------------------------------------------------------------
        self.title(configuration.window_title)

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (configuration.window_width / 2))
        center_y = int((screen_height / 2) - (configuration.window_height / 2))
        self.geometry(f'{configuration.window_width}x{configuration.window_height}+{center_x}+{center_y}')
        self.minsize(configuration.min_window_width, configuration.min_window_height)

        self.Main_Frame = Main_Frame(self, self.event_handler)

        # Place the frames using grid
        self.Main_Frame.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=10, anchor=tk.CENTER)  # Left frame in column 0

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Perform any cleanup or process termination steps here
        # For example, safely terminate any running threads, save state, release resources, etc.

        self.event_handler(Event.ON_CLOSE)

        self.destroy()



class Main_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler

        self.vr_button_state = 0
        self.tdt_button_state = 0

        self.vr_hardware_id = None
        self.vr_connection = bool

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=10, anchor=tk.CENTER)

        self.hardware_connection_frames(top_frame)


    # FRAMES ---------------------------------------------
    def hardware_connection_frames(self, frame):
        # Configure the grid for the frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # TDT Connection Status
        self.tdt_status = ctk.CTkLabel(frame, text=configuration.connection_status_TDT, text_color=configuration.not_connected_color,
                                       font=(configuration.main_font_style, configuration.main_font_size))
        self.tdt_status.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # TDT Reset Button
        self.TDT_button = ctk.CTkButton(frame, text='Connect',
                                        font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.button_fg_color, command=lambda: self.event_handler(Event.TDT_CONNECT))
        self.TDT_button.grid(row=0, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # VR Connection Status
        self.vr_status = ctk.CTkLabel(frame, text=configuration.connection_status_VR, text_color=configuration.not_connected_color,
                                      font=(configuration.main_font_style, configuration.main_font_size))
        self.vr_status.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # VR Reset Button
        self.VR_button = ctk.CTkButton(frame, text='Connect',
                                       font=(configuration.main_font_style, configuration.main_font_size),
                                       fg_color=configuration.button_fg_color, command=lambda: self.event_handler(Event.VR_CONNECT))
        self.VR_button.grid(row=1, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    # BUTTON TOGGLE STATES ------------------------

    def toggle_vr_button(self):
        if self.vr_button_state == 0:
            self.vr_status.configure(text=configuration.connection_status_VR_C,
                                     text_color=configuration.connected_color)
            self.VR_button.configure(text='Disconnect',
                                     fg_color=configuration.stop_fg_color, hover_color=configuration.stop_hover_color,
                                     command=lambda: self.event_handler(Event.VR_DISCONNECT))
            self.vr_button_state += 1
        else:
            self.vr_status.configure(text=configuration.connection_status_VR,
                                     text_color=configuration.not_connected_color)
            self.VR_button.configure(text='Connect',
                                     fg_color=configuration.button_fg_color, hover_color=configuration.button_hover_color,
                                     command=lambda: self.event_handler(Event.VR_CONNECT))
            self.vr_button_state = 0

    def toggle_tdt_button(self):
        if self.tdt_button_state == 0:
            self.tdt_status.configure(text=configuration.connection_status_TDT_C,
                                      text_color=configuration.connected_color)
            self.TDT_button.configure(text='Disconnect',
                                      fg_color=configuration.stop_fg_color, hover_color=configuration.stop_hover_color,
                                      command=lambda: self.event_handler(Event.TDT_DISCONNECT))
            self.tdt_button_state += 1
        else:
            self.tdt_status.configure(text=configuration.connection_status_TDT,
                                      text_color=configuration.not_connected_color)
            self.TDT_button.configure(text='Connect',
                                      fg_color=configuration.button_fg_color, hover_color=configuration.button_hover_color,
                                      command=lambda: self.event_handler(Event.TDT_CONNECT))
            self.tdt_button_state = 0


    # VR HARDWARE VIEWS
    def vr_hardware_connection_status(self):
        self.event_handler(Event.VR_CONNECTION)

        if self.vr_connection:
            self.vr_button_state = 1
            self.toggle_vr_button()
        else:
            self.vr_button_state = 0
            self.toggle_vr_button()

        self.vr_hardware_id = self.after(1000, self.vr_hardware_connection_status)

    def stop_vr_hardware_connection_status(self):
        if self.vr_hardware_id:
            self.after_cancel(self.vr_hardware_id)
            self.vr_hardware_id = None


    # POP UP WINDOWS -------------------------------------------
    def manage_loading_audio_popup(self, text, show=False):
        if show:
            self.loading_popup = tk.Toplevel(self)
            self.loading_popup.title("Loading")
            window_width = 400
            window_height = 100
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            center_x = int((screen_width / 2) - (window_width / 2))
            center_y = int((screen_height / 2) - (window_height / 2))
            self.loading_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
            tk.Label(self.loading_popup, text=text, font=("default_font", 16)).pack(
                pady=10)
            # Configure style for a larger progress bar
            style = ttk.Style(self.loading_popup)
            style.theme_use('clam')  # or 'default', 'classic', 'alt', etc.
            style.configure("Larger.Horizontal.TProgressbar",
                            troughcolor='#D3D3D3',
                            bordercolor='#D3D3D3',
                            background='#00008B',  # Dark Blue color
                            lightcolor='#00008B',  # Adjust if needed
                            darkcolor='#00008B',  # Adjust if needed
                            thickness=30)  # Customize thickness

            self.progress = ttk.Progressbar(self.loading_popup, orient="horizontal", length=250, mode="indeterminate",
                                            style="Larger.Horizontal.TProgressbar")
            self.progress.pack(pady=10)
            self.progress.start()

            def on_close():
                # Perform any necessary cleanup
                self.event_handler(Event.STOP_LOADING)
                self.progress.stop()
                self.loading_popup.destroy()

            self.loading_popup.protocol("WM_DELETE_WINDOW", on_close)

        else:
            if self.loading_popup:
                self.progress.stop()
                self.loading_popup.destroy()

    def close_loading_popup(self):
        try:
            self.manage_loading_audio_popup(text='', show=False)
        except:
            pass

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