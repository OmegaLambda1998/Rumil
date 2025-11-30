from pathlib import Path
from typing import Any

import toml

from rumil._env import ROOT_DIR
from rumil.templates import Template
from rumil.utils.debug import pp


class Note:
    def __init__(self, path: Path, *, force: bool = False, clear: bool = False):
        self.force = force
        self.clear = clear
        self.abs_path = path
        self.rel_path = path.parent.relative_to(ROOT_DIR)
        self.raw = Note.get_raw(path)
        self.frontmatter = Note.get_frontmatter(self.raw)
        self.markdown = Note.get_markdown(self.raw)
        self.templates = Note.get_templates(self.frontmatter)

    @staticmethod
    def get_raw(path: Path) -> str:
        with path.open("r") as io:
            raw = io.read()
        return raw

    @staticmethod
    def get_frontmatter(raw: str) -> dict[str, Any]:
        raw_lines = raw.split("\n")
        toml_lines = []
        in_frontmatter = False
        for line in raw_lines:
            if in_frontmatter:
                if line.strip() == "+++":
                    in_frontmatter = False
                else:
                    toml_lines.append(line)
            elif line.strip() == "+++":
                in_frontmatter = True
        raw_toml = "\n".join(toml_lines)
        frontmatter = toml.loads(raw_toml)
        return frontmatter

    @staticmethod
    def get_markdown(raw: str) -> str:
        markdown_lines = []
        raw_lines = raw.split("\n")
        in_frontmatter = False
        for line in raw_lines:
            if in_frontmatter:
                if line.strip() == "+++":
                    in_frontmatter = False
            elif line.strip() == "+++":
                in_frontmatter = True
            else:
                markdown_lines.append(line)
        markdown = "\n".join(markdown_lines)
        return markdown

    @staticmethod
    def get_templates(frontmatter: dict[str, Any]) -> dict[int, list[Template]]:
        templates = {}
        for id in frontmatter.keys():
            template = Template.templates.get(id)
            if template is None:
                pp(f"Unknown Template: {id}")
            else:
                if template.order not in templates:
                    templates[template.order] = []
                inp = frontmatter[id]
                if isinstance(inp, dict):
                    templates[template.order].append(template(**inp))
                elif isinstance(inp, list):
                    for arg in inp:
                        templates[template.order].append(template(**arg))
        return templates
