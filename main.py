import argparse
from utils.validator import validate_args
from utils.generator import generate_all


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', help='Path to MIDI file to save', required=True)
    parser.add_argument('--seed', help='Random seed', default=None)
    parser.add_argument('--duration', help='Melody duration (in bars)', default=16)
    parser.add_argument('--bpm', help='Tempo (in beats per minute)', default=None)
    parser.add_argument('--key', help='Music key (e.g. C, Dm, F#, Bbm)', default=None)
    parser.add_argument('--snap-interval', help='Snap notes to grid every ... bars', default=4)
    parser.add_argument('--chord-type', help='Type of chords (full/only-root-notes/none)',
                        default='only-root-notes')

    args = parser.parse_args()
    validate_args(vars(args))
    generate_all(vars(args))


if __name__ == '__main__':
    main()
