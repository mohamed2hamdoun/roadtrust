from pathlib import Path

import pytest

from roadtrust.paths import DATA_DIR_ENV, data_dir


def test_default_is_home_folder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(DATA_DIR_ENV, raising=False)
    assert data_dir() == (Path.home() / "roadtrust-data").resolve()


def test_env_var_moves_it(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(DATA_DIR_ENV, str(tmp_path / "ssd"))
    assert data_dir() == (tmp_path / "ssd").resolve()


def test_inside_repo_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    repo = Path(__file__).resolve().parents[2]
    monkeypatch.setenv(DATA_DIR_ENV, str(repo / "data"))
    with pytest.raises(ValueError, match="inside the repository"):
        data_dir()
