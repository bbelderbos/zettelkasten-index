from collections import defaultdict
from pathlib import Path
import re
from typing import NamedTuple, Iterable, Iterator, Mapping, TypeAlias, Sequence

NOTES_DIR = Path.home() / "code" / "experiment" / "code-clnic-zettelkasten"
OUTPUT_FILE = Path("index.md")


class Note(NamedTuple):
    title: str
    file: str


NoteLibrary: TypeAlias = Mapping[str, Sequence[Note]]


def get_note_files(notes_dir: Path) -> Iterator[Path]:
    return notes_dir.glob("*.md")


def group_files_by_tag(files: Iterable[Path]) -> NoteLibrary:
    files_by_tag = defaultdict(list)
    for file in files:
        lines = file.read_text().splitlines()
        title = lines[0].lstrip("# ").capitalize()
        tag_lines = [
            line for line in lines[1:]
            if line.startswith("#")
        ]
        tags = re.findall(r"#\S+", "".join(tag_lines))
        for tag in tags:
            tag = tag.lstrip("#").title()
            files_by_tag[tag].append(
                Note(title=title,
                     file=file.name)
            )
    return files_by_tag


def generate_index_file(
    files_by_tag: NoteLibrary, output_file: Path
) -> None:
    output = ["# Notes index"]
    for tag, notes in sorted(files_by_tag.items()):
        output.append(f"\n## {tag}\n")
        for note in sorted(notes):
            output.append(f"[{note.title}]({note.file})")
    with open(output_file, "w") as f:
        content = "\n".join(output)
        f.write(content)


def create_index(notes_dir: Path = NOTES_DIR,
                 output_file: Path = OUTPUT_FILE) -> None:
    files = get_note_files(notes_dir)
    files_by_tag = group_files_by_tag(files)
    generate_index_file(files_by_tag, output_file)


if __name__ == "__main__":
    create_index()
