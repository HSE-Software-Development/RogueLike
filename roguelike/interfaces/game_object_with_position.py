from __future__ import annotations
from abc import ABC
from roguelike.types import Cell
from .game_object import IGameObject


class IGameObjectWithPosition(IGameObject, ABC):
    cell: Cell
    pickable: bool
    children: list[IGameObjectWithPosition]
