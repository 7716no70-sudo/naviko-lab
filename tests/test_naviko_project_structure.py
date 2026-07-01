from pathlib import Path


def test_naviko_lab_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "navikoLAB").exists()


def test_analyzers_dir_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "navikoLAB" / "analyzers").exists()
