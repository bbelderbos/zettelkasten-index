from pathlib import Path

import pytest

from script import create_index

expected = """# Notes index

## Productivity

[Pybites productivity tips](20220817104440.md)

## Python

[Enumerate](20220817104441.md)
[Pathlib](20220817104442.md)
[Pybites productivity tips](20220817104440.md)
"""

@pytest.fixture
def create_notes(tmp_path):
    note_base = "2022081710444"
    notes = (
        "# Pybites productivity tips\n\nblabla\n\n#productivity #Python",
        "# enumerate\n\nfor i, line in enumerate(lines, start=1):\n\n#python",
        "# pathlib\n\nyou can use home() and cwd() on a Path object\n\n#python"
    )
    for i, note in enumerate(notes):
        file = tmp_path / f"{note_base}{i}.md"
        with open(file, "w") as f:
            f.write(note + "\n")


def test_create_index(tmp_path, create_notes):
    output_file = tmp_path / "index.md"
    create_index(notes_dir=tmp_path, output_file=output_file)
    with open(output_file) as f:
        content = f.read().strip()
    assert content == expected.strip()
