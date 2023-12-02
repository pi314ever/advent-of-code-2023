from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"


def get_data_path(filename):
    return DATA_DIR / filename
