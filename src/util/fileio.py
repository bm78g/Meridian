from pathlib import Path

def get_files(dir):
    files = [f for f in Path(dir).iterdir() if f.is_file()]
    return files