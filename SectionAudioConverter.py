import math
import numpy as np
import mido
from ImageSectionSelector import ImageSelectionSelector
from VideoMaker import VideoMaker as VM, VideoMaker
from pydub import AudioSegment

soundFilePath = "Sounds/ImageMusic.wav"


class SectionAudioConverter:
    def __init__(self, chanelCount = 1, scale_down_factor=4):
        self.scale_down_factor = scale_down_factor
        self.volume = 64
        self.trackTempo = 1000
        self.trackInstrumental = mido.MidiTrack()
        self.mid = mido.MidiFile()

        self.mid.tracks.append(self.trackInstrumental)
        self.trackInstrumental.append(mido.MetaMessage('set_tempo', tempo=self.trackTempo))

        self.IS = ImageSelectionSelector("m108", 4, 0, 0, self.scale_down_factor)
        self.sps = 44100
        self.freq_hz = 220.0
        self.duration = 0.1
        self.vol = 1
        self.esm = np.arange(self.duration * self.sps)

        self.trackSynth = AudioSegment.empty()

        self.chanelCount = chanelCount + 1
        self.VM = VideoMaker(1 / self.duration)

    def InstrumentalConvert(self):
        secList = self.IS.get_sections()

        while len(secList) != 0:
            for section in secList:
                distanceFromCenter = math.sqrt(math.pow(section.x_pos, 2) + math.pow(section.y_pos, 2))
                if distanceFromCenter > 200:
                    distanceFromCenter = 200
                program_change = mido.Message('program_change', program=section.z_pos, channel=0)
                self.trackInstrumental.append(program_change)
                self.trackInstrumental.append(
                    mido.Message('note_on', note=section.intensity % 5, velocity=self.volume, time=0))
                self.trackInstrumental.append(
                    mido.Message('note_off', note=section.intensity % 5, velocity=self.volume, time=1))
            '''
            for section in secList:
                distanceFromCenter = math.sqrt(math.pow(section.x_pos, 2) + math.pow(section.y_pos, 2))
                self.trackInstrumental.append(mido.Message('note_off', note=int(section.intensity / 2), velocity=self.volume, channel=1, time=distanceFromCenter))
            '''
            secList = self.IS.get_sections()

        self.mid.save(soundFilePath)

    def fun(self, x, a):
        return a * np.sin(x)

    def SynthConvert(self):

        global ListOfTracks

        ListOfSect = self.IS.get_sections()
        ListOfTracks = [AudioSegment.empty()] * self.chanelCount

        while len(ListOfSect) != 0:
            for chanel in range(1, self.chanelCount):
                print(chanel)
                dominantIntensity = 0
                for section in ListOfSect:
                    dominantIntensity += math.pow(1.05, section.intensity)
                dominantIntensity /= len(ListOfSect)

                currentFreq = self.freq_hz + chanel * dominantIntensity
                currentVol = self.vol
                waveFunction = self.fun((2 * np.pi * self.esm * currentFreq / self.sps), dominantIntensity)
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

SAC = SectionAudioConverter(4, scale_down_factor=4)
SAC.SynthConvert()

VM = VideoMaker(fps=10)
VM.audio_path = "Sounds/ImageMusic.wav"
VM.gen_video("combined")
VM.gen_video("grid")
