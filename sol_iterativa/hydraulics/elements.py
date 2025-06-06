import abc
from typing import List, Optional
from abc import ABC


class Element(ABC):
    def __init__(self, name: str) -> None:
        self._name = name
        self._next = [None, None]

    @property
    def name(self) -> str:
        return self._name

    def connect(self, elm: "Element") -> None:
        self._next[0] = elm

    @property
    def output(self) -> Optional["Element"]:
        return self._next[0]

    def simulate(flow_in, to_explore):
        pass

    def get_simulation_str(self, flow_in, *flow_outs):
        sim_str = "{} {} {:.3f}".format(type(self).__name__, self.name, flow_in)
        if flow_outs:
            flow_outs = " ".join(["{:.3f}".format(f) for f in flow_outs])
            sim_str = sim_str + " " + flow_outs
        return sim_str


class Source(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._flow = None

    @property
    def flow(self) -> float:
        return self._flow

    @flow.setter
    def flow(self, flow: float) -> None:
        self._flow = flow

    def simulate(self, flow_in, to_explore):
        to_explore.append((self.output, self.flow))
        return self.get_simulation_str(0, self._flow)


class Tap(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._status = False

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, to_open: bool = True) -> None:
        self._status = to_open

    def simulate(self, flow_in, to_explore):
        flow_out = flow_in if self.status else 0
        to_explore.append((self.output, flow_out))
        return self.get_simulation_str(flow_in, flow_out)


class Sink(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def connect(self, elm: "Element") -> None:
        pass

    def simulate(self, flow_in, to_explore):
        return self.get_simulation_str(flow_in, 0)


class Split(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def connect_at(self, elm: Element, pos: int) -> None:
        self._next[pos] = elm

    @property
    def outputs(self) -> List[Optional[Element]]:
        return self._next

    def simulate(self, flow_in, to_explore):
        flow_out = flow_in / 2
        for output in self.outputs:
            if output:
                to_explore.append((output, flow_out))
        return self.get_simulation_str(flow_in, flow_out, flow_out)


class MultiSplit(Split):
    def __init__(self, name: str, num_out: int) -> None:
        super().__init__(name)
        self._next = [None]*num_out
        self._propotions = None

    @property
    def proportions(self) -> List[Optional[float]]:
        return self._propotions

    @proportions.setter
    def proportions(self, proportions: List[Optional[float]]) -> None:
        self._propotions = proportions

    def simulate(self, flow_in, to_explore):
        out_flows = [flow_in * p for p in self._propotions]
        for output, flow_out in zip(self.outputs, out_flows):
            to_explore.append((output, flow_out))
        return self.get_simulation_str(flow_in, *out_flows)
