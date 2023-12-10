from typing import Protocol


class _LenSupport(Protocol):
    def __len__(self) -> int:
        ...


class GridDataType(Protocol):
    N: int
    M: int
    data: list[_LenSupport]

    def __getitem__(self, key: tuple[int, int]) -> _LenSupport:
        ...
