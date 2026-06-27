"""Shared utility helpers for project scripts."""

from __future__ import annotations

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if needed and return it as a Path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def format_currency(value: float) -> str:
    """Format a numeric value for business-facing reports."""
    return f"{value:,.2f}"


def write_lines(path: str | Path, lines: list[str]) -> Path:
    """Write one line per item to a UTF-8 text file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path

