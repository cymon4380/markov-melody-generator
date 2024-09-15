def validate_args(args: dict):
    if not 1 <= int(args.get('duration')) <= 256:
        raise ValueError('Duration must be between 1 and 256')
    if not 1 <= int(args.get('snap_interval')) <= 256:
        raise ValueError('Snap interval must be between 1 and 256')
    if args.get('bpm') is not None:
        if not 20 <= int(args.get('bpm')) <= 240:
            raise ValueError('BPM must be between 20 and 240')
    if args.get('chord_type') not in ['full', 'only-root-notes', 'none']:
        raise ValueError('Invalid value: chord-type')
