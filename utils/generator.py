import random
import numpy as np
from models.music import Note, MidiChannel, Harmony, MusicFile
from models.music import notes as _notes
from utils.music import parse_key, get_scale
from utils.seed_converter import convert as convert_seed


melody_matrix = np.array([
    [.1, .2, .3, .1, .1, .1, .05, .05],
    [.2, .1, .3, .2, .1, .05, .05, 0],
    [.3, .3, .1, .2, .05, .05, 0, 0],
    [.2, .1, .2, .1, .3, .05, .05, 0],
    [.1, .2, .05, .3, .1, .2, .05, 0],
    [.1, .05, .2, .05, .2, .1, .3, 0],
    [.05, .05, .1, .05, .3, .2, .1, .15],
    [.1, .05, .15, .05, .15, .2, .15, .15]
])

chords_matrix = np.array([
    [.1, .2, .1, .2, .3, .1],
    [.1, .05, .1, .3, .3, .15],
    [.05, .2, .05, .2, .2, .3],
    [.3, .15, .05, .1, .3, .1],
    [.3, .15, .1, .2, .2, .05],
    [.3, .15, .1, .2, .2, .05]
])


def generate_melody(
        scale: list[int],
        seed=None,
        duration: int = 8,
        snap_interval: int = 4
) -> list[Note]:
    notes = []
    rnd = random.Random(seed)

    if seed is not None:
        np_seed = convert_seed(seed)
        np.random.seed(np_seed)

    note_index = random.choice(range(len(scale)))
    position = 0
    duration_eighths = duration * 8
    snap_interval_eights = snap_interval * 8

    while position < duration_eighths:
        offset = scale[note_index]
        length = rnd.randint(1, 4)
        maximum_note_length = snap_interval_eights - position % snap_interval_eights

        if maximum_note_length < 4:
            length = maximum_note_length

        notes.append(Note(
            offset=offset,
            position=position,
            length=length,
            midi_channel=MidiChannel.Melody
        ))
        position += length

        note_index = np.random.choice(range(len(scale)), p=melody_matrix[note_index])

    return notes


def generate_chords(
    scale: list[int],
    harmony: Harmony,
    seed=None,
    duration: int = 8,
    snap_interval: int = 4,
    only_root_notes: bool = False
) -> list[Note]:
    notes = []
    rnd = random.Random(seed)

    if seed is not None:
        np_seed = convert_seed(seed)
        np.random.seed(np_seed)

    scale = scale[:6]

    note_index = random.choice(range(len(scale)))
    position = 0
    duration_eights = duration * 8
    snap_interval_eights = snap_interval * 8
    lengths = [2, 4, 6, 8, 12]

    while position < duration_eights:
        offset = scale[note_index]
        length = rnd.choice(lengths)
        maximum_note_length = snap_interval_eights - position % snap_interval_eights

        if maximum_note_length < 12:
            length = maximum_note_length

        ignore_index = 6 if harmony == Harmony.Major else 1
        major_indexes = [0, 3, 4] if harmony == Harmony.Major else [2, 5, 6]

        chord_note_index = note_index if note_index != ignore_index else rnd.randint(0, 2)
        chord_harmony = Harmony.Major if chord_note_index in major_indexes else Harmony.Minor
        middle_note_offset = 4 if chord_harmony == Harmony.Major else 3
        chord_notes = []

        for note_offset in [0] if only_root_notes else [0, middle_note_offset, 7]:
            chord_notes.append(scale[chord_note_index] + note_offset)

        notes.append(Note(
            offset=offset,
            position=position,
            length=length,
            midi_channel=MidiChannel.Chords,
            chord_notes=chord_notes
        ))

        position += length
        note_index = np.random.choice(range(len(scale)), p=chords_matrix[note_index])

    return notes


def generate_all(args: dict):
    seed = args.get('seed')
    rnd = random.Random(seed)

    bpm = int(args.get('bpm') or rnd.randint(90, 180))
    duration = int(args.get('duration'))
    snap_interval = int(args.get('snap_interval'))

    if args.get('key'):
        tonic, harmony = parse_key(args.get('key'))
    else:
        tonic = rnd.choice(list(_notes.keys()))
        alt_sign = rnd.choice(['', '#', 'b'])
        if (alt_sign == '#' and tonic not in ['E', 'B']) or (alt_sign == 'b' and tonic not in ['C', 'F']):
            tonic += alt_sign

        harmony = rnd.choice(list(Harmony))

    print(f"BPM: {bpm}")
    print(f"Key: {tonic} {harmony.name.lower()}")

    scale = get_scale(tonic, harmony)

    print('-' * 32)
    melody_notes = generate_melody(scale=scale, seed=seed, duration=duration, snap_interval=snap_interval)
    chord_notes = None

    if args.get('chord_type') != 'none':
        chord_notes = generate_chords(
            scale=scale,
            harmony=harmony,
            seed=seed,
            duration=duration,
            snap_interval=snap_interval,
            only_root_notes=args.get('chord_type') == 'only-root-notes'
        )

    print('Generation complete!')
    file = MusicFile(bpm=bpm)
    file.add_track(melody_notes)

    if chord_notes:
        file.add_track(chord_notes)

    filename = args.get('file').strip('.')
    if not filename.endswith('.mid'):
        filename += '.mid'

    midi = file.to_midi()
    midi.save(filename)

    print(f"Saved to {filename}")
