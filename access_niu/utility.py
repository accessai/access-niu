import os


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)