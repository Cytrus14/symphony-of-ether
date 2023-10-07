import math

import mido
from ImageSection import ImageSection as IS

volume = 64
trackTempo = 1000
track = mido.MidiTrack()
mid = mido.MidiFile()
sectionList = None

class SectionAudioConverter:
    def __init__(self, trackTempo):
        mid.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=trackTempo))

    def ToMidi(self):
        while(sectionList is not None):
            sectionsList = IS.GetSections()
            for section in sectionList:
                distanceFromCenter = math.sqrt(math.pow(section.x, 2) + math.pow(section.y))
                if distanceFromCenter > 200:
                    distanceFromCenter = 200
                program_change = mido.Message('program_change', program=section.z, channel=0)
                track.append(program_change)
                note_on = mido.Message('note_on', note=section.intensity, velocity=volume, channel=0)
                track.append(note_on)
                track.append(mido.Message('note_off'), note=section.intensity, velocity=volume, channel=0, time=distanceFromCenter)
        mid.save("ImageMusic.mid")

