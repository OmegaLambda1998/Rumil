from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from rumil.notes import Note


class Template:
    templates: ClassVar[dict[str, type["Template"]]] = {}
    id: ClassVar[str] = ""
    order: ClassVar[int] = -1
    unique: ClassVar[bool] = False

    @classmethod
    def register(cls) -> None:
        cls.templates[cls.id] = cls

    def __init__(self, *args, **kwargs):
        pass

    def pre_apply_to(self, note: "Note"):
        pass

    def apply_to(self, note: "Note"):
        pass

    def post_apply_to(self, note: "Note"):
        pass
