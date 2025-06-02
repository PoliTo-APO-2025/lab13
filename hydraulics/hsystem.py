from hydraulics.elements import Element, Source
from typing import List


class HSystem:
    def __init__(self) -> None:
        pass

    def add_element(self, elm: Element) -> None:
        pass

    @property
    def elements(self) -> List[Element]:
        pass

    def simulate(self) -> List[str]:
        pass
