import mido

class SectionAudioConverter:

    def __init__(self, xPos, yPos, zPos, intensity, trackTempo):
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.intensity = intensity
        self.trackTempo = trackTempo
        track = mido.MidiTrack()
        mid = mido.MidiFile()
        mid.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=trackTempo))


    def ToMidi(self):
        program_change = mido.Message('program_change', program=27, channel=0)
