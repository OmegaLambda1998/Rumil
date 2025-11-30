from dataclasses import dataclass
from pathlib import Path
from rumil.templates.template import Template
from typing import TYPE_CHECKING
from shutil import copyfile
from rumil._env import CONFIGURATIONS_DIR

if TYPE_CHECKING:
    from rumil.notes import Note


@dataclass
class Configuration:
    config: Path
    path: Path


class Configurations(Template):
    id = "configurations"

    def __init__(self, *args, configuration: list[dict] | None = None, **kwargs):
        if configuration is None:
            configuration = []
        self.configs = [Configuration(**config) for config in configuration]
        super().__init__(*args, **kwargs)

    def post_apply_to(self, note: "Note"):
        super().post_apply_to(note)

        for configuration in self.configs:
            path = note.abs_path.parent / configuration.path
            config = configuration.config
            if not config.is_absolute():
                config = CONFIGURATIONS_DIR / config
            config = Path.resolve(config)
            if path.exists():
                if not note.force:
                    print(
                        f"{self.id}: Can't {'rm' if note.clear else 'overwrite'} {path}"
                    )
                    return
            if note.clear:
                if path.exists():
                    print(f"{self.id}: Removing {path}")
                    path.unlink()
            else:
                print(f"{self.id}: Copying {config} to {path}")
                copyfile(config, path)


Configurations.register()
