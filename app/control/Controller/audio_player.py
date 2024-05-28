
import sounddevice as sd
import numpy as np




def play_audio_on_computer(audio_sample, **kwargs):
    gain_value = kwargs.get('gain')
    audio_samples = audio_sample.data
    if gain_value is not None:
        audio_samples = audio_sample.data * np.round((gain_value / 100), 2)

    sd.play(audio_samples, audio_sample.sample_rate)


def stop_audio_on_computer():
    sd.stop()