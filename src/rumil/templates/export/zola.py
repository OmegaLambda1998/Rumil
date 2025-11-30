from .export import Export
from typing import TYPE_CHECKING
import toml

if TYPE_CHECKING:
    from rumil.notes import Note


class ExportZola(Export):
    id = "zola"
    export_id = "zola"

    def __init__(self, *args, path: str | None = None, **kwargs):
        if path is None:
            path = "_index.md"
        super().__init__(*args, path=path, **kwargs)

    def pre_apply_to(self, note: "Note"):
        note.markdown = "+++\n" + toml.dumps(note.frontmatter) + "+++\n" + note.markdown

        super().pre_apply_to(note)


ExportZola.register_export()
