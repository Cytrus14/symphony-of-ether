import mido
from ImageSection import ImageSection as IS

track = mido.MidiTrack()
mid = mido.MidiFile()
SectionList = None

class SectionAudioConverter:
    def __init__(self, IS, trackTempo):
        SectionsList = IS.GetSections()
        mid.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=trackTempo))

    def ToMidi(self):
        program_change = mido.Message('program_change', program=27, channel=0)
        track.append(program_change)
