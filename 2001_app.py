import audiocore
import audiobusio
import array
from buttons import Buttons

class level:
    def __init__(self, device: audiobusio.I2SOut, buttons: Buttons) -> None:
        self.device = device
        self.buttons = buttons

        #setup beep
        sample_rate = 100000
        tone_volume = .05  # Increase or decrease this to adjust the volume of the tone.
        frequency = 440  # Set this to the Hz of the tone you want to generate.
        length = sample_rate // frequency  # One freqency period
        sine_wave = array.array("H", [0] * length)
        for i in range(length):
            sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                                tone_volume + 1) * (2 ** 15 - 1))
        self.sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=sample_rate)

        self.wave_file = open("2001.wav", "rb")
        self.wave = audiocore.WaveFile(self.wave_file)

    def play(self):
        self.device.play(self.wave)

    def stop(self):
        self.device.play(self.sine_wave_sample)

    def update(self):
        if self.buttons.B:
            if self.device.playing:
                self.stop()
            else:
                self.play()
    
    def exit(self):
        self.stop()
