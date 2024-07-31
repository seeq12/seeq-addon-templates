from pathlib import Path
from utils import create_virtual_environment


PROJECT_PATH = Path(__file__).parent.resolve()

create_virtual_environment(PROJECT_PATH, clean=True)
