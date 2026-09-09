"""MkDocs hooks used by this repository."""

import importlib.util
from pathlib import Path


_module_path = Path(__file__).with_name("update_index.py")
_spec = importlib.util.spec_from_file_location("update_index", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load {_module_path}")
_update_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_update_index)


def on_pre_build(*, config, **kwargs) -> None:
    """Ensure newly added articles appear on the home page before each build."""
    _update_index.update_index()
