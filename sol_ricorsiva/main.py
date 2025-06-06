from hydraulics.hsystem import HSystem
from hydraulics.elements import Source, Tap, Sink, Split, MultiSplit


def main():
    # create HSystem
    h_sys = HSystem()

    # create elements
    src_1 = Source("Source_1")
    tap_1 = Tap("Tap_1")
    spl_1 = Split("Split_1")
    snk_1 = Sink("Sink_1")
    snk_2 = Sink("Sink_2")

    # add elements to System
    h_sys.add_element(src_1)
    h_sys.add_element(tap_1)
    h_sys.add_element(spl_1)
    h_sys.add_element(snk_1)
    h_sys.add_element(snk_2)

    # get elements and print list of their names
    print("Elements in the system:")
    print([e.name for e in h_sys.elements])     # ['Source_1', 'Tap_1', 'Split_1', 'Sink_1', 'Sink_2']

    # connect elements
    src_1.connect(tap_1)
    tap_1.connect(spl_1)
    spl_1.connect_at(snk_1, 0)
    spl_1.connect_at(snk_2, 1)

    # get outputs
    print("Outputs:")
    print(src_1.output.name if src_1.output is not None else None)    # Tap_1
    print(tap_1.output.name if tap_1.output is not None else None)    # Split_1
    print([e.name for e in spl_1.outputs if e is not None])           # ['Sink_1', 'Sink_2']

    # set simulation parameters
    src_1.flow = 11.5
    tap_1.status = True

    # start simulation
    print("First simulation:")
    print(h_sys.simulate())
    # [
    #     'Source Source_1 0.000 11.500',
    #     'Tap Tap_1 11.500 11.500',
    #     'Split Split_1 11.500 5.750 5.750',
    #     'Sink Sink_1 5.750 0.000',
    #     'Sink Sink_2 5.750 0.000'
    # ]

    # close tap and run another simulation
    tap_1.status = False
    print("Second simulation:")
    print(h_sys.simulate())
    # [
    #     'Source Source_1 0.000 11.500',
    #     'Tap Tap_1 11.500 0.000',
    #     'Split Split_1 0.000 0.000 0.000',
    #     'Sink Sink_1 0.000 0.000',
    #     'Sink Sink_2 0.000 0.000'
    # ]

    # create multi-split
    mult_1 = MultiSplit("Multi_1", 3)
    mult_1.proportions = [0.3, 0.6, 0.1]    # [0.3, 0.6, 0.1]
    print(mult_1.proportions)

    # simulate system with multi-split
    h_sys_2 = HSystem()

    src_2 = Source("Source_2")
    src_2.flow = 10.0
    snk_3 = Sink("Sink_3")
    snk_4 = Sink("Sink_4")
    snk_5 = Sink("Sink_5")

    src_2.connect(mult_1)
    mult_1.connect_at(snk_3, 0)
    mult_1.connect_at(snk_4, 1)
    mult_1.connect_at(snk_5, 2)

    h_sys_2.add_element(src_2)
    h_sys_2.add_element(snk_3)
    h_sys_2.add_element(snk_4)
    h_sys_2.add_element(snk_5)
    h_sys_2.add_element(mult_1)

    print(h_sys_2.simulate())
    # [
    #     'Source Source_2 0.000 10.000',
    #     'MultiSplit Multi_1 10.000 3.000 6.000 1.000',
    #     'Sink Sink_3 3.000 0.000', 'Sink Sink_4 6.000 0.000',
    #     'Sink Sink_5 1.000 0.000'
    # ]


if __name__ == "__main__":
    main()
