import math
import numpy as np
import mido
from ImageSection import ImageSection as IS
from pydub import AudioSegment

sectionList = None

soundFilePath = "Sounds/ImageMusic.wav"

class SectionAudioConverter:
    def __init__(self, trackTempo):
        volume = 64
        trackTempo = 1000
        self.trackInstrumental = mido.MidiTrack()
        mid = mido.MidiFile()

        sps = 44100
        freq_hz = 220.0
        duration = 2
        vol = 0.3
        esm = np.arange(duration * sps)

        mid.tracks.append(self.trackInstrumental)
        self.trackInstrumental.append(mido.MetaMessage('set_tempo', tempo=trackTempo))
        self.trackSynth = AudioSegment.empty()

    def InstrumentalConvert(self):
        while(sectionList is not None):
            sectionsList = IS.GetSections()
            for section in sectionList:
                distanceFromCenter = math.sqrt(math.pow(section.x, 2) + math.pow(section.y))
                if distanceFromCenter > 200:
                    distanceFromCenter = 200
                program_change = mido.Message('program_change', program=section.z, channel=0)
                self.trackInstrumental.append(program_change)
                note_on = mido.Message('note_on', note=section.intensity, velocity=self.volume, channel=0)
                self.trackInstrumental.append(note_on)

            for section in sectionsList:
                distanceFromCenter = math.sqrt(math.pow(section.x, 2) + math.pow(section.y))
                self.trackInstrumental.append(mido.Message('note_off'), note=section.intensity, velocity=self.volume, channel=section.id, time=distanceFromCenter)
        self.mid.save(soundFilePath)

    def fun(self, x, a, b, c, d):
        return a * np.sin(x) * np.sin(x) * np.sin(x) + b * np.sin(x) * np.sin(x) + c * np.sin(x) + d

    def SythConvert(self):
        for section in sectionList:
            waveFunction = self.fun((2 * np.pi * self.esm * self.freq_hz / self.sps), section.x, section.y, section.z, 0)
            waveFunctionQuiet = waveFunction * self.vol
            waveFunctionInt = np.int16(waveFunctionQuiet * 32767)

            new_segment = AudioSegment(
                waveFunctionInt.tobytes(),
                frame_rate=self.sps,
                sample_width=2,  # 16-bit
                channels=section.id  # Mono
            )

            self.trackSynth += new_segment
            self.trackSynth.export(soundFilePath, format="wav")


