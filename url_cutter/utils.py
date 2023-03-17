from hashlib import md5


def get_hash(text):
    return md5(text.encode()).hexdigest()[:16]


