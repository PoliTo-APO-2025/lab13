import unittest
from hydraulics.hsystem import HSystem
from hydraulics.elements import Source, Tap, Split, Sink, MultiSplit


class TestR1(unittest.TestCase):

    def setUp(self):
        self._tap = Tap("tap")
        self._source = Source("src")
        self._sink = Sink("sink")
        self._split = Split("split")

    def test_get_name(self):
        self.assertEqual(self._tap.name, "tap")
        self.assertEqual(self._source.name, "src")
        self.assertEqual(self._sink.name, "sink")
        self.assertEqual(self._split.name, "split")

    def test_add_get(self):
        h = HSystem()
        h.add_element(self._tap)
        h.add_element(self._source)
        h.add_element(self._sink)
        h.add_element(self._split)
        self.assertTrue(self._tap in h.elements)
        self.assertTrue(self._source in h.elements)
        self.assertTrue(self._sink in h.elements)
        self.assertTrue(self._split in h.elements)


class TestR2(unittest.TestCase):

    def setUp(self):
        self._tap = Tap("tap")
        self._source = Source("src")
        self._sink = Sink("sink")

    def test_connect(self):
        self._source.connect(self._tap)
        self._tap.connect(self._sink)
        self.assertIs(self._source.output, self._tap)
        self.assertIs(self._tap.output, self._sink)

    def test_connect_sink(self):
        self._sink.connect(self._tap)
        self.assertIs(self._sink.output, None)

    def test_get_outputs_none(self):
        self.assertIs(self._source.output, None)
        self.assertIs(self._tap.output, None)


class TestR3(unittest.TestCase):

    def setUp(self):
        self._tap = Tap("tap")
        self._sink = Sink("sink")
        self._split = Split("split")

    def test_connect_at(self):
        self._split.connect_at(self._tap, 0)
        self._split.connect_at(self._sink, 1)
        outputs = self._split.outputs
        self.assertIs(outputs[0], self._tap)
        self.assertIs(outputs[1], self._sink)

    def test_connect_at_none(self):
        self._split.connect_at(self._tap, 0)
        outputs = self._split.outputs
        self.assertIs(outputs[0], self._tap)
        self.assertIs(outputs[1], None)


class TestR4(unittest.TestCase):

    def setUp(self):
        self._source = Source("src")
        self._tap = Tap("tap")
        self._split = Split("split")
        self._sink1 = Sink("sink1")
        self._sink2 = Sink("sink2")

        self._hsys = HSystem()
        self._hsys.add_element(self._source)
        self._hsys.add_element(self._tap)
        self._hsys.add_element(self._split)
        self._hsys.add_element(self._sink1)
        self._hsys.add_element(self._sink2)

    def test_simple_test_open(self):
        self._source.connect(self._tap)
        self._tap.connect(self._sink1)
        self._source.flow = 4.789
        self._tap.status = True
        info = self._hsys.simulate()
        self.assertEqual(len(info), 3)
        self.assertTrue('Source src 0.000 4.789' in info)
        self.assertTrue('Tap tap 4.789 4.789' in info)
        self.assertTrue('Sink sink1 4.789 0.000' in info)

    def test_simple_test_close(self):
        self._source.connect(self._tap)
        self._tap.connect(self._sink1)
        self._source.flow = 4.789
        self._tap.status = False
        info = self._hsys.simulate()
        self.assertEqual(len(info), 3)
        self.assertTrue('Source src 0.000 4.789' in info)
        self.assertTrue('Tap tap 4.789 0.000' in info)
        self.assertTrue('Sink sink1 0.000 0.000' in info)

    def test_simple_test_split(self):
        self._source.connect(self._split)
        self._split.connect_at(self._sink1, 0)
        self._split.connect_at(self._sink2, 1)
        self._source.flow = 6.789
        info = self._hsys.simulate()
        self.assertEqual(len(info), 4)
        self.assertTrue('Source src 0.000 6.789' in info)
        self.assertTrue('Split split 6.789 3.394 3.394' in info)
        self.assertTrue('Sink sink1 3.394 0.000' in info)
        self.assertTrue('Sink sink2 3.394 0.000' in info)

    def test_all_elements(self):
        self._source.connect(self._tap)
        self._tap.connect(self._split)
        self._split.connect_at(self._sink1, 0)
        self._split.connect_at(self._sink2, 1)
        self._source.flow = 7
        self._tap.status = True
        info = self._hsys.simulate()
        self.assertEqual(len(info), 5)
        self.assertTrue('Source src 0.000 7.00 in info')
        self.assertTrue('Tap tap 7.000 7.000' in info)
        self.assertTrue('Split split 7.000 3.500 3.500' in info)
        self.assertTrue('Sink sink1 3.500 0.000' in info)
        self.assertTrue('Sink sink2 3.500 0.000' in info)


class TestR5(unittest.TestCase):

    def setUp(self):
        self._source = Source("src")
        self._tap = Tap("tap")
        self._multi = MultiSplit("multi", 3)
        self._sink1 = Sink("sink1")
        self._sink2 = Sink("sink2")
        self._sink3 = Sink("sink3")

        self._hsys = HSystem()
        self._hsys.add_element(self._source)
        self._hsys.add_element(self._tap)
        self._hsys.add_element(self._multi)
        self._hsys.add_element(self._sink1)
        self._hsys.add_element(self._sink2)
        self._hsys.add_element(self._sink3)

    def test_proportions(self):
        self._multi.proportions = [0.1, 0.2, 0.7]
        self.assertEqual([0.1, 0.2, 0.7], self._multi.proportions)

    def test_multi_outputs(self):
        self._multi.connect_at(self._sink1, 0)
        self._multi.connect_at(self._sink3, 2)
        outs = self._multi.outputs
        self.assertIs(self._sink1, outs[0])
        self.assertIs(None, outs[1])
        self.assertIs(self._sink3, outs[2])

    def test_all_elements(self):
        self._source.connect(self._tap)
        self._tap.connect(self._multi)
        self._multi.connect_at(self._sink1, 0)
        self._multi.connect_at(self._sink2, 1)
        self._multi.connect_at(self._sink3, 2)
        self._source.flow = 9
        self._tap.status = True
        self._multi.proportions = [0.5, 0.3, 0.2]
        info = self._hsys.simulate()
        self.assertEqual(len(info), 6)
        self.assertTrue('Source src 0.000 9.00 in info')
        self.assertTrue('Tap tap 9.000 9.000' in info)
        self.assertTrue('MultiSplit multi 9.000 4.500 2.700 1.800' in info)
        self.assertTrue('Sink sink1 4.500 0.000' in info)
        self.assertTrue('Sink sink2 2.700 0.000' in info)
        self.assertTrue('Sink sink3 1.800 0.000' in info)

    def test_all_tap_closed(self):
        self._source.connect(self._tap)
        self._tap.connect(self._multi)
        self._multi.connect_at(self._sink1, 0)
        self._multi.connect_at(self._sink2, 1)
        self._multi.connect_at(self._sink3, 2)
        self._source.flow = 9
        self._tap.status = False
        self._multi.proportions = [0.5, 0.3, 0.2]
        info = self._hsys.simulate()
        self.assertEqual(len(info), 6)
        self.assertTrue('Source src 0.000 9.00 in info')
        self.assertTrue('Tap tap 9.000 0.000' in info)
        self.assertTrue('MultiSplit multi 0.000 0.000 0.000 0.000' in info)
        self.assertTrue('Sink sink1 0.000 0.000' in info)
        self.assertTrue('Sink sink2 0.000 0.000' in info)
        self.assertTrue('Sink sink3 0.000 0.000' in info)

