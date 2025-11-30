from .export import Export
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rumil.notes import Note


class ExportREADME(Export):
    id = "readme"
    export_id = "readme"

    def __init__(self, *args, path: str | None = None, **kwargs):
        if path is None:
            path = "README.md"
        super().__init__(*args, path=path, **kwargs)

    def pre_apply_to(self, note: "Note"):
        note.markdown += "# {% title %}\n\n{% description %}"

        super().pre_apply_to(note)


ExportREADME.register_export()
