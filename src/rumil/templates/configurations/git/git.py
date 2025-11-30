from rumil.templates.configurations import Configurations
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    pass


class Git(Configurations):
    id = "git"

    git_templates: ClassVar[dict[str, type["Git"]]] = {}
    git_id: ClassVar[str] = ""

    @classmethod
    def register_git(cls) -> None:
        cls.git_templates[cls.git_id] = cls

    def __new__(cls, *args, configuration: list[dict] | None = None, **kwargs):
        for key in kwargs:
            if key in cls.git_templates:
                cls = cls.git_templates.get(key, cls)
                return super().__new__(cls)
        return super().__new__(cls)

    def __init__(self, *args, configuration: list[dict] | None = None, **kwargs):
        super().__init__(*args, configuration=configuration, **kwargs)


Git.register()
