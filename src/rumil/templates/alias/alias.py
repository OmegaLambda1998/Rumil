from rumil.templates.template import Template
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rumil.notes import Note


class Alias(Template):
    id = "alias"
    order = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aliases = {}
        for alias, value in kwargs.items():
            self.aliases[f"{{% {alias} %}}"] = value

    def apply_to(self, note: "Note"):
        super().apply_to(note)

        for alias, value in self.aliases.items():
            if alias in note.markdown:
                note.markdown = note.markdown.replace(alias, value)


Alias.register()
