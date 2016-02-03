'''
    Generating random Graphs basing on Erdos-Renyi model
    https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model
'''
import random


class Graph(object):
    def __init__(self, n, p, w=1):
        '''
            Creates a new `DataStructure` representing a graph
            with `n` vertices (labeled with incremental integers)
            and probability of connection `p`.
            The weight of the edge will be at maximum `w` (uniformly
            distributed).
        '''
        self.n = n
        self.p = p
        self.w = w
        self.data = self._generate(n, p, w)

    def _generate(self, n, p, w):
        '''
            Generates  and returns it the internal representation
        '''
        pass

    def insert(self, edge):
        '''
            Creates and edge (a couple) between
            `edge[0]` and `edge[1]`.
        '''
        pass

    def delete(self, edge):
        '''
            Deletes the edge (if it exists) between
            `edge[0]` and `edge[1]`.
        '''
        pass

    def find(self, edge):
        '''
            Returns if `edge[0]` and `edge[1]` are connected.
        '''
        pass

    def enumerate(self, vertex):
        '''
            Returns the neighbors of `vertex`
        '''
        pass


class AdjMatrixGraph(Graph):
    def __repr__(self):
        r = '\t'
        r += '\t'.join([str(i) for i in xrange(self.n)])
        r += '\n\t'
        r += '\t'.join(['|' for i in xrange(self.n)])
        r += '\n'

        for i, row in enumerate(self.data):
            r += str(i) + ' --\t'
            r += '\t'.join([str(el) for el in row])
            r += '\n'

        return r

    def _generate(self, n, p, w):
        m = [[0 for _ in xrange(n)] for _ in xrange(n)]

        for i in xrange(n - 1):
            for j in xrange(i + 1, n):
                if random.random() < p:
                    m[i][j] = random.randint(1, w)
                    m[j][i] = m[i][j]

        # we have to ensure that each vertex has at least
        # one connection
        for i, row in enumerate(m):
            if not any(row):
                vertices = range(i) + range(i + 1, n)
                j = random.choice(vertices)
                m[i][j] = random.randint(1, w)
                m[j][i] = m[i][j]

        return m

    def insert(self, edge):
        i = edge[0]
        j = edge[1]
        self.data[i][j] = random.randint(1, self.w)
        self.data[j][i] = self.data[i][j]

    def delete(self, edge):
        i = edge[0]
        j = edge[1]
        self.data[i][j] = 0
        self.data[j][i] = 0

    def find(self, edge):
        i = edge[0]
        j = edge[1]
        return self.data[i][j] > 0

    def enumerate(self, vertex):
        return [(i, v) for i, v in enumerate(self.data[vertex]) if v > 0]


class AdjListGraph(Graph):
    def __repr__(self):
        r =''

        for i, row in enumerate(self.data):
            r += str(i) + ' --\t'
            r += '\t'.join([str(el) for el in row])
            r += '\n'

        return r

    def _generate(self, n, p, w):
        m = [[] for _ in xrange(n)]

        for i in xrange(n - 1):
            for j in xrange(i + 1, n):
                if random.random() < p:
                    connected = True
                    val = random.randint(1, w)
                    m[i].append((j, val))
                    m[j].append((i, val))

        # we have to ensure that each vertex has at least
        # one connection
        for i, row in enumerate(m):
            if len(row) == 0:
                vertices = range(i) + range(i + 1, n)
                j = random.choice(vertices)
                val = random.randint(1, w)
                m[i].append((j, val))
                m[j].append((i, val))

        return m

    def insert(self, edge):
        if self.find(edge):
            # the edge is already there
            return

        i = edge[0]
        j = edge[1]
        w = random.randint(1, self.w)
        self.data[i].append((j, w))
        self.data[j].append((i, w))

    def delete(self, edge):
        i = edge[0]
        j = edge[1]

        if self.find(edge):
            ni = [v[0] for v in self.data[i]]
            nj = [v[0] for v in self.data[j]]
            del self.data[i][ni.index(j)]
            del self.data[j][nj.index(i)]

    def find(self, edge):
        i = edge[0]
        j = edge[1]
        return j in [el[0] for el in self.data[i]]

    def enumerate(self, vertex):
        return self.data[vertex]

