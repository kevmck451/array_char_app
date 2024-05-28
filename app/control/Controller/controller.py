
from app.control.Controller.events import Event
from app.control.Controller.client import Sender_Client
from app.control.Controller.audio_abstract import Audio_Abstract
import app.control.Controller.audio_player as comp_audio
from app.docs.resources import base_path


import threading
from pathlib import Path

class Controller:
    def __init__(self):
        self.client = None
        self.gui = None
        self.waiting_for_connection = False
        self.hardware_connected = False


    def set_gui(self, gui):
        self.gui = gui

    # EVENT HANDLER FUNCTION
    # -----------------------------
    def handle_event(self, event):

        if event == Event.ON_CLOSE:
            print('controller shutting down')
            if self.client is not None:
                self.client.close_connection()

        elif event == Event.CONNECT_HARDWARE:
            self.client = Sender_Client(name='MacBook')
            self.gui.hardware_state = 0
            self.gui.toggle_hardware_connect()
            self.waiting_for_connection = True
            wait_for_connection_thread = threading.Thread(target=self.wait_for_connection, daemon=True)
            wait_for_connection_thread.start()

        elif event == Event.DISCONNECT_HARDWARE:
            self.waiting_for_connection = False
            self.client.close_connection()
            self.gui.hardware_state = 2
            self.gui.toggle_hardware_connect()

        elif event == Event.PLAY_AUDIO:
            print('playing audio')
            self.gui.toggle_play()

            # Find the matching file path or None if not found
            filepath = next((path for path in self.gui.file_list if Path(path).stem == self.gui.current_file_selection), None)

            if filepath:
                audio = Audio_Abstract(filepath=filepath, num_channels=1)

                if self.hardware_connected:
                    # use TDT hardware
                    pass
                else:
                    gain = self.gui.knob.get()
                    comp_audio.play_audio_on_computer(audio, gain=gain)

            else:
                self.gui.warning_popup_general('Error with filepath')




        elif event == Event.STOP_AUDIO:
            print('stopping audio')
            self.gui.toggle_play()
            if self.hardware_connected:
                # use TDT hardware
                pass
            else:
                comp_audio.stop_audio_on_computer()

    # OTHER FUNCTIONS
    # -----------------------------

    def wait_for_connection(self):
        while self.waiting_for_connection:
            if self.client.connected:
                self.gui.hardware_state = 1
                self.gui.toggle_hardware_connect()
                self.connected()


    def connected(self):
        self.hardware_connected = True







