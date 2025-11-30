import click
from pathlib import Path
from ._env import ROOT_DIR, NOTE_FILE
from .rumil import main


def get_paths(input_path: Path, *, recursive: bool):
    paths: list[Path] = []
    if input_path.is_file():
        if input_path.stem + input_path.suffix == NOTE_FILE:
            paths.append(input_path)
        elif not recursive:
            print(f"{input_path} is not a {NOTE_FILE} file")
    else:
        if recursive:
            for path in input_path.iterdir():
                paths += get_paths(path, recursive=recursive)
        else:
            path = input_path / NOTE_FILE
            if path.exists():
                paths.append(path)
            elif not recursive:
                print(f"{input_path} does not contain a {NOTE_FILE} file")
    return paths


@click.command
@click.argument(
    "input_path", type=click.Path(exists=True, path_type=Path), default=ROOT_DIR
)
@click.option("-r", "--recursive", is_flag=True, type=bool, default=False)
@click.option("-f", "--force", is_flag=True, type=bool, default=False)
@click.option("-c", "--clear", is_flag=True, type=bool, default=False)
def cli(
    input_path: Path,
    *,
    recursive: bool = False,
    force: bool = False,
    clear: bool = False,
):
    paths = get_paths(input_path, recursive=recursive)
    for path in paths:
        main(path, force=force, clear=clear)


if __name__ == "__main__":
    cli()
