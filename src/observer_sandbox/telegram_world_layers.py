from __future__ import annotations

from . import telegram_world_layers_base as _base
from .telegram_world_layers_item_extension import install_item_world_layers_extension

install_item_world_layers_extension(_base)

for _name in _base.__all__:
    globals()[_name] = getattr(_base, _name)

__all__ = list(_base.__all__)


def __getattr__(name: str):
    return getattr(_base, name)
