import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

static = os.path.join(BASE_DIR, 'static')

print(static)
