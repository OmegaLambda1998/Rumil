from rumil.templates.template import Template
from rumil._env import ROOT_DIR
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from rumil.notes import Note


class Export(Template):
    id = "export"
    export_templates: ClassVar[dict[str, type["Export"]]] = {}
    export_id: ClassVar[str] = ""
    unique = True

    @classmethod
    def register_export(cls) -> None:
        cls.export_templates[cls.export_id] = cls

    def __new__(cls, *args, template: str, path: str | None = None, **kwargs):
        cls = cls.export_templates.get(template, cls)
        return super().__new__(cls)

    def __init__(self, *args, template: str, path: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = Path(path)

    def post_apply_to(self, note: "Note"):
        super().post_apply_to(note)

        path = self.path
        if not path.is_absolute():
            path = ROOT_DIR / note.rel_path / path
        path = Path.resolve(path)

        if path.exists():
            if not note.force:
                print(f"{self.id}: Can't {'rm' if note.clear else 'overwrite'} {path}")
                return
        if note.clear:
            if path.exists():
                print(f"{self.id}: Removing {path}")
                path.unlink()
        else:
            print(f"{self.id}: Writing {path}")
            with path.open("w") as io:
                io.write(note.markdown)


Export.register()
