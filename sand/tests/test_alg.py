from unittest import TestCase
from sand.graph import AdjMatrixGraph
from sand import dijkstra, bf

class AlgorithmsTestCase(TestCase):
    def setUp(self):
        self.graph = AdjMatrixGraph(100, 0.6)

    def test_dijkstra_is_same_as_bf_if_w_is_1(self):
        bf_res = bf.run(self.graph, 0)
        dj_res = dijkstra.run(self.graph, 0)

        self.assertEqual(bf_res, dj_res)

