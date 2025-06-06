from hydraulics.elements import Element, Source
from typing import List


class HSystem:
    def __init__(self) -> None:
        self._elements = []

    def add_element(self, elm: Element) -> None:
        self._elements.append(elm)

    @property
    def elements(self) -> List[Element]:
        return self._elements

    def simulate(self) -> List[str]:
        simulation_lst = []
        to_explore = []
        for elm in self._elements:
            if isinstance(elm, Source):
                to_explore.append((elm, None))
                break
            
        while to_explore:
            elm, flow_in = to_explore.pop(0)
            sim_str = elm.simulate(flow_in, to_explore)
            simulation_lst.append(sim_str)
        return simulation_lst


