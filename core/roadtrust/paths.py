"""Filesystem locations shared by every RoadTrust component (ADR15)."""

import os
from pathlib import Path

DATA_DIR_ENV = "ROADTRUST_DATA_DIR"
DEFAULT_DATA_DIR = "~/roadtrust-data"
_REPO = Path(__file__).resolve().parents[2]


def data_dir() -> Path:
    """Root folder for datasets, simulator output and chain data.

    Set ROADTRUST_DATA_DIR to move it (for example to an external SSD). The folder must be
    outside the repository so a dataset can never be committed by accident.
    """
    path = Path(os.environ.get(DATA_DIR_ENV) or DEFAULT_DATA_DIR).expanduser().resolve()
    if (_REPO / ".git").exists() and path.is_relative_to(_REPO):
        raise ValueError(
            f"{DATA_DIR_ENV}={path} is inside the repository {_REPO}; "
            "data must live outside git (ADR15)"
        )
    return path
