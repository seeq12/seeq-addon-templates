import sys
from pathlib import Path
from addon_template._dev_tools.utils import create_virtual_environment


PROJECT_PATH = Path(__file__).parent.resolve()

# The first argument is always the script name
path = sys.argv[1] if len(sys.argv) > 1 else None
if path:
    PROJECT_PATH = Path(path).resolve()
create_virtual_environment(PROJECT_PATH, clean=True, hide_stdout=True)
