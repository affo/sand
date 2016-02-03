from unittest import TestCase
from sand.graph import AdjMatrixGraph

class AdjMatrixTestCase(TestCase):
    def setUp(self):
        self.graph = AdjMatrixGraph(10, 0.5)

    def test_insert(self):
        self.graph.insert((0, 1))
        self.assertTrue(self.graph.find((1, 0)))
        self.assertTrue(self.graph.find((0, 1)))

    def test_is_connected(self):
        for row in self.graph.data:
            self.assertTrue(any(row))

    def test_delete(self):
        edge = (0, 1)
        redge = (1, 0)

        self.graph.insert(edge)
        self.assertTrue(self.graph.find(edge))
        self.assertTrue(self.graph.find(redge))

        self.graph.delete(edge)
        self.assertFalse(self.graph.find(edge))
        self.assertFalse(self.graph.find(redge))

    def test_neighbors(self):
        edge = (0, 1)

        self.graph.insert(edge)
        n0 = self.graph.enumerate(edge[0])
        n1 = self.graph.enumerate(edge[1])

        n0 = [v[0] for v in n0]
        n1 = [v[0] for v in n1]

        self.assertTrue(edge[1] in n0)
        self.assertTrue(edge[0] in n1)

