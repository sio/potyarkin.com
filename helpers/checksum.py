'''Calculate checksum of a file'''

from hashlib import sha256


def hash(filepath):
    checksum = sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(2**10), bytes()):
            checksum.update(chunk)
    return checksum.hexdigest()
