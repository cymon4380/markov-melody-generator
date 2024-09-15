import hashlib


def convert(seed: str) -> int:
    return int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16) % (2 ** 32)
