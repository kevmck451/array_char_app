# Hardware Controller File


from app.hardware.Model.tdt_hardware.TDT_manager import TDT_Circuit
from app.hardware.Controller.states import State
from app.hardware.Controller.time_class import time_class
from app.hardware.Model.server.server import Server
from app.hardware.Controller.events import Event


from threading import Thread
import threading





class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.tdt_hardware = TDT_Circuit()
        self.audio_loading = False
        self.server_running = False
        self.gain_values = None
        self.server = None

    def set_gui(self, gui):
        self.gui = gui

    # These are the gate keepers for whether or not to perform the action
    def handle_event(self, event):
        # TDT HARDWARE EVENTS
        # -----------------------------------
        if event == Event.TDT_CONNECT:
            if self.app_state == State.IDLE:
                self.app_state = State.TDT_INITIALIZING
                self.start_tdt_hardware()

        elif event == Event.TDT_DISCONNECT:
            if self.app_state == State.IDLE:
                self.app_state = State.TDT_INITIALIZING
                self.tdt_hardware.disconnect_hardware()
                self.gui.Main_Frame.toggle_tdt_button()
                self.app_state = State.IDLE


        # SERVER EVENTS
        # -----------------------------------
        elif event == Event.START_HARDWARE_SERVER:
            if self.app_state == State.IDLE:
                self.app_state = State.SERVER_INITIALIZING
                self.start_server()

        elif event == Event.SERVER_DISCONNECT:
            if self.app_state == State.IDLE:
                self.app_state = State.SERVER_INITIALIZING
                self.server_running = False
                self.server.stop()
                self.gui.Main_Frame.toggle_server_button()
                self.gui.Main_Frame.server_running = False
                self.gui.Main_Frame.change_server_status()
                self.app_state = State.IDLE

        elif event == Event.CONTROLLER_CONNECTED:
            print('controller connected')
            self.gui.Main_Frame.server_running = True
            self.gui.Main_Frame.change_server_status()

        elif event == Event.CONTROLLER_DISCONNECTED:
            print('controller disconnected')
            self.gui.Main_Frame.server_running = False
            self.gui.Main_Frame.change_server_status()

        elif event == Event.PLAY_AUDIO:
            # pass along audio to play
            # send gain values
            # self.tdt_hardware.play_audio_speaker_array()
            pass


        elif event == Event.STOP_AUDIO:
            pass

        # UTILITY EVENTS
        # -----------------------------------
        # Window Closing Actions
        elif event == Event.ON_CLOSE:
            if self.tdt_hardware.circuit_state:
                self.tdt_hardware.disconnect_hardware()
                self.server.stop()

        # Loading Box was Closed
        elif event == Event.STOP_LOADING:
            if self.app_state == State.TDT_INITIALIZING:
                self.tdt_hardware.initialize = False


    # Action Functions ------------------------------
    def start_tdt_hardware(self):
        self.gui.Main_Frame.manage_loading_audio_popup(text='Waiting for Connection...', show=True)
        load_thread = Thread(target=self.wait_for_tdt_connection, daemon=True)
        load_thread.start()

    def wait_for_tdt_connection(self):
        connection_time = time_class('connection_time')
        self.tdt_hardware.initialize = True
        load_thread = Thread(target=self.tdt_hardware.connect_hardware, daemon=True)
        load_thread.start()
        wait_time = 40
        while self.tdt_hardware.circuit_state == False:
            if self.tdt_hardware.initialize == False:
                break
            if connection_time.reaction_time() > wait_time:
                print(f'connection timed out at {wait_time} secs')
                break

        self.gui.Main_Frame.close_loading_popup()
        if self.tdt_hardware.circuit_state:
            self.gui.Main_Frame.toggle_tdt_button()
        else:
            if self.tdt_hardware.initialize:
                self.gui.Main_Frame.warning_popup_general(message='connection could not be made')

        self.tdt_hardware.initialize = False
        self.app_state = State.IDLE

    def start_server(self):
        # set for simulation connection with 0.0.0.0 if testing
        # self.server = Server('0.0.0.0')
        self.server = Server()
        self.server.set_controller(self)
        event_thread = threading.Thread(target=self.server.run, daemon=True)
        event_thread.start()
        self.gui.Main_Frame.toggle_server_button()
        self.app_state = State.IDLE




