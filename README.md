# Markov Melody Generator
This app generates melodies with Markov chains and saves them to MIDI files.

---

## Usage
```
python main.py --file FILE [--seed SEED] [--duration DURATION] [--bpm BPM] [--key KEY] [--snap-interval SNAP_INTERVAL] [--chord-type CHORD_TYPE]
```

**Required parameters**
- `--file` - Output file

**Optional parameters**
- `--seed` - Random seed
- `--duration` - Duration of melody (in bars) _(default: 16)_
- `--bpm` - Tempo (in beats per minute) _(default: random)_
- `--key` - Music key (e.g. `C`, `Dm`, `F#`, `Bbm`) _(default: random)_
- `--snap-interval` - Snap notes to grid every ... bars _(default: 4)_
- `--chord-type` - Type of chords (`none` / `only-root-notes` / `full`) _(default: only-root-notes)_

### Example
```
python main.py --file output.mid --duration 32 --bpm 135 --key G#
```