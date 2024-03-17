import audiocore
import audiobusio
import audiomixer
import math
import array

from buttons import Buttons
from display import Display
from app_base import AppBase

class PlayerApp(AppBase):
    def __init__(
        self, device: audiobusio.I2SOut, buttons: Buttons, display: Display
    ) -> None:
        self.device = device
        self.buttons = buttons
        self.display = display
        self.first = True

        # setup beep
        sample_rate = 100000
        tone_volume = (
            0.05  # Increase or decrease this to adjust the volume of the tone.
        )
        frequency = 440  # Set this to the Hz of the tone you want to generate.
        length = sample_rate // frequency  # One freqency period
        sine_wave = array.array("H", [0] * length)
        for i in range(length):
            sine_wave[i] = int(
                (math.sin(math.pi * 2 * frequency * i / sample_rate) * tone_volume + 1)
                * (2**15 - 1)
            )
        self.sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=sample_rate)

        self.wave_file = open("2001.wav", "rb")
        self.wave = audiocore.WaveFile(self.wave_file)
        self.mixer = audiomixer.Mixer(
            voice_count=1,
            sample_rate=self.wave.sample_rate,
            channel_count=self.wave.channel_count,
            bits_per_sample=self.wave.bits_per_sample,
            samples_signed=True,
        )

    def entry(self):
        self.stop()
        self.showVol()
        self.first = False

    def play(self):
        self.display.printLine("Press B to Stop", 1)
        self.device.play(self.mixer)
        self.mixer.voice[0].play(self.wave)

    def stop(self):
        self.display.printLine("Press B to Play", 1)
        self.device.stop()

    def showVol(self):
        self.display.printLine(
            "Vol: {0:3.0f}%".format(self.mixer.voice[0].level * 100), 3
        )

    def update(self, dt: float):
        if self.first:
            self.entry()
        if self.buttons.B_pressed:
            if self.device.playing:
                self.stop()
            else:
                self.play()
        if self.buttons.up:
            newVol = self.mixer.voice[0].level + 0.01
            if newVol <= 1.0:
                self.mixer.voice[0].level = newVol
                self.showVol()
        if self.buttons.down:
            newVol = self.mixer.voice[0].level - 0.01
            if newVol >= 0.0:
                self.mixer.voice[0].level = newVol
                self.showVol()

    def exit(self):
        self.first = True
        self.stop()
