from __future__ import annotations

import json
import re
from pathlib import Path


NOTEBOOK_METADATA = {
    "kernelspec": {
        "display_name": ".venv",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.10",
    },
}


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def empty_code_cell() -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [],
    }


def split_on_heading(lines: list[str], prefix: str) -> list[list[str]]:
    sections: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if line.startswith(prefix) and current:
            sections.append(current)
            current = []
        current.append(line)

    if current:
        sections.append(current)

    return sections


def normalize_math_delimiters(text: str) -> str:
    # Some notebook renderers only interpret dollar-delimited LaTeX reliably.
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)
    return text


def build_cells(markdown_text: str) -> list[dict]:
    markdown_text = normalize_math_delimiters(markdown_text)
    top_sections = split_on_heading(markdown_text.splitlines(keepends=True), "## ")
    cells: list[dict] = []

    for section in top_sections:
        section_text = "".join(section).strip("\n")
        if not section_text:
            continue

        if section[0].startswith("## Explicit task list"):
            task_sections = split_on_heading(section, "### ")
            intro = "".join(task_sections[0]).strip("\n")
            if intro:
                cells.append(markdown_cell(intro + "\n"))

            for task_section in task_sections[1:]:
                task_text = "".join(task_section).strip("\n")
                if not task_text:
                    continue
                cells.append(markdown_cell(task_text + "\n"))
                cells.append(empty_code_cell())
            continue

        cells.append(markdown_cell(section_text + "\n"))

        if section[0].startswith("## Stretch tasks"):
            cells.append(empty_code_cell())

    return cells


def convert_markdown_file(markdown_path: Path) -> Path:
    notebook = {
        "cells": build_cells(markdown_path.read_text(encoding="utf-8")),
        "metadata": NOTEBOOK_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    notebook_path = markdown_path.with_suffix(".ipynb")
    notebook_path.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return notebook_path


def main() -> None:
    workshop_dir = Path(__file__).resolve().parent
    markdown_files = sorted(workshop_dir.glob("*.md"))

    for markdown_path in markdown_files:
        notebook_path = convert_markdown_file(markdown_path)
        print(f"Generated {notebook_path.relative_to(workshop_dir.parent)}")


if __name__ == "__main__":
    main()
