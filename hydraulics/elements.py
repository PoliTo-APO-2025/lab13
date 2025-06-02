import abc
from typing import List, Optional
from abc import ABC


class Element(ABC):
    def __init__(self, name: str) -> None:
        pass

    @property
    def name(self) -> str:
        pass

    def connect(self, elm: "Element") -> None:
        pass

    @property
    def output(self) -> Optional["Element"]:
        pass


class Source(Element):
    def __init__(self, name: str) -> None:
        pass

    @property
    def flow(self) -> float:
        pass

    @flow.setter
    def flow(self, flow: float) -> None:
        pass


class Tap(Element):
    def __init__(self, name: str) -> None:
        pass

    @property
    def status(self) -> bool:
        pass

    @status.setter
    def status(self, to_open: bool = True) -> None:
        pass


class Sink(Element):
    def __init__(self, name: str) -> None:
        pass


class Split(Element):
    def __init__(self, name: str) -> None:
        pass

    def connect_at(self, elm: Element, pos: int) -> None:
        pass

    @property
    def outputs(self) -> List[Optional[Element]]:
        pass


class MultiSplit(Split):
    def __init__(self, name: str, num_out: int) -> None:
        pass

    @property
    def proportions(self) -> List[Optional[float]]:
        pass

    @proportions.setter
    def proportions(self, proportions: List[Optional[float]]) -> None:
        pass
