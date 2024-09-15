from models.music import notes, Harmony


def get_note_offset(note: str) -> int:
    offset = notes[note[0]]

    if note.endswith('#'):
        offset += 1
    elif note.endswith('b'):
        offset -= 1

    return offset % 12


def get_scale(tonic: str, harmony: Harmony) -> list[int]:
    scale = [get_note_offset(tonic)]

    for offset in harmony.value:
        scale.append(scale[-1] + offset)

    return scale


def parse_key(key: str) -> tuple[str, Harmony]:
    tonic, harmony = (key[:-1], Harmony.Minor) if key.endswith('m') else (key, Harmony.Major)

    get_note_offset(tonic)
    return tonic, harmony
