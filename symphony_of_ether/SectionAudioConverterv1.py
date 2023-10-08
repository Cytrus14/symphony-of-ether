import math
import noisereduce as nr
import soundfile as sf
import numpy as np
from pydub import AudioSegment

from symphony_of_ether.ImageSectionSelector import ImageSelectionSelector
from symphony_of_ether.VideoMaker import VideoMaker

soundFilePath = "Sounds/ImageMusic.wav"


def fun(x, a):
    wave = a * np.sinc(x)
    return 20 - 1/wave


class SectionAudioConverter:
    def __init__(self, x_pos=50, y_pos=50, z_pos=1, scale_down_factor=4, imageName="m108"):
        self.imageName = imageName
        self.sps = 44100
        self.freq_hz = 100.0
        self.duration = 0.1
        self.vol = 1
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        self.scale_down_factor = scale_down_factor
        self.IS = ImageSelectionSelector(self.imageName, 4, start_x=self.x_pos, start_y=self.y_pos,
                                         scale_down_factor=self.scale_down_factor)
        self.esm = np.arange(self.duration * self.sps)

        self.trackSynth = AudioSegment.empty()

        self.chanelCount = z_pos + 1
        self.VM = VideoMaker(1 / self.duration)

    def SynthConvert(self):
        ListOfSect = self.IS.get_sections()
        ListOfTracks = [AudioSegment.empty()] * self.chanelCount

        #print("Loading sound...")
        while len(ListOfSect) != 0:
            for chanel in range(1, self.chanelCount):
                dominantIntensity = 0
                for section in ListOfSect:
                    dominantIntensity += math.pow(1.2, section.intensity)
                dominantIntensity /= len(ListOfSect)

                currentFreq = (self.freq_hz + chanel * dominantIntensity)/(chanel*2)
                currentVol = self.vol
                waveFunction = fun((2 * np.pi * self.esm * currentFreq / self.sps), dominantIntensity)
                waveFunctionQuiet = waveFunction * currentVol
                waveFunctionInt = np.int16(waveFunctionQuiet * 32767)

                new_segment = AudioSegment(
                    waveFunctionInt.tobytes(),
                    frame_rate=self.sps,
                    sample_width=2,  # 16-bit
                    channels=1  # Mono
                )

                ListOfTracks[chanel] += new_segment
            ListOfSect = self.IS.get_sections()

        finalTrack = AudioSegment.empty()
        for t in ListOfTracks:
            finalTrack = t.overlay(finalTrack)

        finalTrack.export(soundFilePath, format="wav")

        audio_data, sample_rate = sf.read(soundFilePath)
        reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
        sf.write(soundFilePath, reduced_noise, sample_rate)

'''
SAC = SectionAudioConverter(4, scale_down_factor=4)
SAC.SynthConvert()

VM = VideoMaker(fps=10)
VM.audio_path = "Sounds/ImageMusic.wav"
VM.gen_video("combined")
VM.gen_video("grid")
'''