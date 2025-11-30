import os
from pathlib import Path

NOTE_FILE = ".rumil.md"

ROOT_DIR = Path(os.environ.get("ROOT_DIR", Path.home()))
PROJECTS_DIR = Path(os.environ.get("PROJECTS_DIR", ROOT_DIR / "Projects"))
AREAS_DIR = Path(os.environ.get("AREAS_DIR", ROOT_DIR / "Areas"))
CONFIGURATIONS_DIR = Path(
    os.environ.get("CONFIGURATIONS_DIR", AREAS_DIR / "Configurations")
)
RESOURCES_DIR = Path(os.environ.get("RESOURCES_DIR", ROOT_DIR / "Resources"))
ARCHIVE_DIR = Path(os.environ.get("ARCHIVE_DIR", ROOT_DIR / "Archive"))

RUMIL_DIR = Path("/tmp/rumil")
RUMIL_DIR.mkdir(parents=True, exist_ok=True)
