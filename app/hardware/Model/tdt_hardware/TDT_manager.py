
import sounddevice as sd
import numpy as np
import time
import os


class TDT_Circuit:
    def __init__(self):

        # random = np.random.choice([True, False])
        # if random: self.circuit_state = True
        # else: self.circuit_state = False
        self.circuit_state = False
        self.initialize = False
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        new_path = os.path.join(current_script_dir, 'tdt_circuit_2.rcx')
        self.RPvds_circuit_filepath = new_path

        self.num_speakers = 36

        # instantiate the gain values in a list of num_speakers
        self.gain_values = np.zeros(self.num_speakers, dtype=int)


    def connect_hardware(self):
        while self.initialize:
            try:
                print('connecting')
                from tdt import DSPProject
                print('imported')
                project = DSPProject()
                self.circuit = project.load_circuit(
                    circuit_name = self.RPvds_circuit_filepath,
                    device_name = 'RX8')
                self.circuit.start()

                if self.circuit.is_connected:
                    self.circuit_state = True
                    self.initialize = False
                    print('connected')
                    break
                else:
                    self.circuit_state = False

            except Exception as e:
                print('connection attempt failed')
                self.circuit_state = False
                time.sleep(1)


    def disconnect_hardware(self):
        self.circuit.stop()
        self.circuit_state = False


    def set_gain(self):
        for i , gain_value in enumerate(self.gain_values):
            if gain_value > 100: gain_value = 100
            if gain_value < 0: gain_value = 0
            scaled_gain = np.round((gain_value / 100), 2)
            self.circuit.set_tag(f"ch{i+1}_gain", scaled_gain)

    @staticmethod
    def play_audio_on_computer(audio_sample, **kwargs):
        gain_value = kwargs.get('gain')
        audio_samples = audio_sample.data
        if gain_value is not None:
            audio_samples = audio_sample.data * np.round((gain_value / 100), 2)

        sd.play(audio_samples, audio_sample.sample_rate)
        time.sleep(audio_sample.sample_length)


    def play_audio_speaker_array(self, audio_sample):
        self.set_gain()

        speaker_buffer = self.circuit.get_buffer(data_tag='speaker', mode='w')
        speaker_buffer.set(audio_sample.data)

        self.circuit.trigger(trigger=1)

        time.sleep(audio_sample.sample_length)


    def stop_audio_speaker_array(self):
        self.circuit.stop()



if __name__ == '__main__':
    from app.docs.resources import base_path
    from app.hardware.Model.data_manager.audio_abstract import Audio_Abstract

    audio_filepath = base_path('audio_files/white_noise.wav')
    audio = Audio_Abstract(filepath=audio_filepath)

    hardware = TDT_Circuit()

    # hardware.play_audio_on_computer(audio, gain=100)

    hardware.initialize = True
    hardware.connect_hardware()




    # hardware.play_audio_speaker_array(white_noise)
    # hardware.stop_audio_speaker_array()

    '''
    # play sound
    hardware.play_audio_speaker_array(audio)
    # change gain values
    for i in range(30):
        hardware.gain_values[i-1] = 0
        hardware.gain_values[i] = 65
        time.sleep(3)

    hardware.stop_audio_speaker_array()
    '''