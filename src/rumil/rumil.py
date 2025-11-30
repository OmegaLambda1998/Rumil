from pathlib import Path
from .notes import Note


def main(path: Path, *, force: bool = False, clear: bool = False):
    note_ = Note(path, force=force, clear=clear)
    notes: dict[str, Note] = {}
    for order in sorted(note_.templates.keys(), reverse=True):
        for template in note_.templates[order]:
            if template.unique:
                notes[template.id] = Note(path, force=force, clear=clear)
    for id, note in notes.items():
        for order in sorted(note.templates.keys(), reverse=True):
            for template in note.templates[order]:
                if (not template.unique) or template.id == id:
                    template.pre_apply_to(note)
        for order in sorted(note.templates.keys(), reverse=True):
            for template in note.templates[order]:
                if (not template.unique) or template.id == id:
                    template.apply_to(note)
        for order in sorted(note.templates.keys(), reverse=True):
            for template in note.templates[order]:
                if (not template.unique) or template.id == id:
                    template.post_apply_to(note)
