from .git import Git
from typing import TYPE_CHECKING
from rumil._env import CONFIGURATIONS_DIR, RUMIL_DIR

GITIGNORE_DIR = CONFIGURATIONS_DIR / "git" / "gitignore"

if TYPE_CHECKING:
    pass


class GitIgnore(Git):
    id = "git.ignore"
    git_id = "ignore"

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        inp = kwargs.get("ignore", {})
        templates = inp.get("templates", [])
        paths = inp.get("paths", [])

        templates = ["Default"] + templates
        gitignore = ""
        if len(paths) > 0:
            gitignore += "# === Custom ===\n" + "\n".join(paths) + "\n\n"
        for template in templates:
            gitignore += f"# === {template} ===\n"
            file = GITIGNORE_DIR / f"{template}.gitignore"
            with file.open("r") as io:
                gitignore += io.read()
            gitignore += "\n"
        with (RUMIL_DIR / ".gitignore").open("w") as io:
            io.write(gitignore)

        configuration = [{"config": RUMIL_DIR / ".gitignore", "path": ".gitignore"}]
        super().__init__(*args, configuration=configuration, **kwargs)


GitIgnore.register_git()
