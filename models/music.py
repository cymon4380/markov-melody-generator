from mido import MetaMessage, Message, MidiFile, MidiTrack, bpm2tempo
from enum import Enum


notes = {
    'A': 0,
    'B': 2,
    'C': 3,
    'D': 5,
    'E': 7,
    'F': 8,
    'G': 10
}


class Harmony(Enum):
    Major = [2, 2, 1, 2, 2, 2, 1]           # In semitones
    Minor = [2, 1, 2, 2, 1, 2, 2]


class MidiChannel(Enum):
    Melody = 0
    Chords = 1


class Note:
    def __init__(
        self,
        offset: int,
        position: int,
        length: int,
        midi_channel: MidiChannel,
        velocity: int = 100,
        chord_notes: list = None
    ):
        self.offset = offset                # Offset from A4 (in semitones)
        self.position = position            # Position (in eighths)
        self.length = length                # Length (in eighths)
        self.midi_channel = midi_channel
        self.velocity = velocity            # 0-127
        self.chord_notes = chord_notes or []

    @staticmethod
    def get_midi_offset(offset: int, octave: int = 5) -> int:
        return offset + 12 * octave - 3


class MusicFile:
    def __init__(self, bpm: int):
        self.bpm = bpm
        self.notes = []
        self.tracks = []

    def add_track(self, note_list: list[Note]):
        track = MidiTrack()
        self.notes += note_list
        self.tracks.append(track)

        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))
        track.append(MetaMessage('time_signature', numerator=4, denominator=4))

        for note in note_list:
            sub_notes = note.chord_notes or [note.offset]
            octave = 3 if note.chord_notes else 5

            for sub_note in sub_notes:
                track.append(Message(
                    'note_on',
                    note=Note.get_midi_offset(sub_note, octave),
                    velocity=note.velocity,
                    time=0,
                    channel=note.midi_channel.value
                ))

            for i in range(len(sub_notes)):
                track.append(Message(
                    'note_off',
                    note=Note.get_midi_offset(sub_notes[i], octave),
                    time=note.length * 240 if i == 0 else 0,
                    channel=note.midi_channel.value
                ))

    def to_midi(self) -> MidiFile:
        mid = MidiFile()
        mid.tracks += self.tracks

        return mid
