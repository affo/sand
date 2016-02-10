INF = float('inf')

key = 1
val = 0
debug = False

class Heap:
    def __init__(self, N):
        self.heap = []
        self.maxlength = N
        self.position = {}
    # end

    def __repr__(self):
        return str(self.heap)
    # end

    def empty(self):
        return 0 == len(self.heap)
    # end

    def getKey(self, n):
        return self.heap[self.position[n]][1]
    # end

    def length(self):
        return len(self.heap)

    def insert(self, v):
        if len(self.heap) < self.maxlength:
            element = (v, self.key(v))
            self.heap.append(element)
            i = self.heap.index(element)
            self.heapifyUp(i)
            self.position[v] = self.heap.index(element)
        else:
            print "full heap, cannot add ", v
            return -1
    # end

    def insert_key(self, v, k):
        if len(self.heap) < self.maxlength:
            element = (v, k)
            self.heap.append(element)
            i = self.heap.index(element)
            self.heapifyUp(i)
            self.position[v] = self.heap.index(element)
        else:
            print "full heap, cannot add ", v
            return -1
    # end

    def findMin(self):
        return self.heap[0]
    # end

    def delete(self, i):
        # substitute the element in i with the last one
        if debug:
            print "Remove element %i from position %i" % (self.heap[i][0], i)
        if i == len(self.heap) - 1:
            del self.position[self.heap[i][0]]
            return self.heap.pop()
        else:
            if debug:
                print "Put element %i from position %i in %i" % (self.heap[len(self.heap)-1][0], len(self.heap)-1, i)
            deleted = self.heap[i]
            self.heap[i] = self.heap.pop()

            del self.position[deleted[0]]

            left_index = 2 * i + 1
            right_index = 2 * (i + 1)

            if self.heap[i][key] < self.heap[i/2][key]:
                self.heapifyUp(i)
            elif (left_index < len(self.heap) and self.heap[i][key] > self.heap[left_index][key]):
                self.heapifyDown(i)
            elif (right_index < len(self.heap) and self.heap[i][key] > self.heap[right_index][key]):
                self.heapifyDown(i)
            else:
                self.position[self.heap[i][val]] = i
                if debug:
                    print "It is an heap"

            return deleted
    # end

    def extractMin(self):
        return self.delete(0)
    # end

    def heapifyUp(self, i):
        v = self.heap[i]
        if debug:
            print "heapifyUp %f, in position %f with key %f" % (v[val], i, v[key])
        if i > 0:
            j = i/2
            p = self.heap[j]
            if v[key] < p[key]:
                if debug:
                    print "We need to re-heap"
                self.heap[i] = p
                self.heap[j] = v
                self.position[p[val]] = i
                self.position[v[val]] = j
                self.heapifyUp(j)
        else:
            self.position[v[val]] = i
            if debug:
                print 'It is an heap'
    # end

    def heapifyDown(self, i):
        v = self.heap[i]
        index_left = 2 * i + 1
        index_right = 2 * (i + 1)
        if debug:
            if debug:
                print "heapifyDown %f, from position %f with key %f" % (v[val], i, v[key])
        if 2 * i + 1 > self.length() or 2 * (i + 1) > self.length():
            if debug:
                print "%i is a leaf, this is an heap" % i
            return
        elif index_left < len(self.heap) and index_right < len(self.heap):

            key_left = self.heap[index_left][key]
            key_right = self.heap[index_right][key]

            if key_left is not None and key_right is not None:
                if key_right > key_left:
                    j = index_left
                else:
                    j = index_right
        elif index_left < len(self.heap) and not index_right < len(self.heap):
            j = index_left
        elif index_right < len(self.heap) and not index_left < len(self.heap):
            j = index_right
        else:
            j = 2 * i

        v = self.heap[i]
        w = self.heap[j]
        if w[key] < v[key]:
            self.heap[j] = v
            self.heap[i] = w
            self.position[w[val]] = i
            self.position[v[val]] = j
            self.heapifyDown(j)

    def changeKey(self, n, k):
        i = self.position[n]
        v = self.heap[i]
        self.heap[i] = (v[0], k)

        left_index = 2 * i + 1
        right_index = 2 * (i + 1)

        if debug:
            print "New element in position %i is %r" % (i, self.heap[i])
        if k < self.heap[i/2][key]:
            self.heapifyUp(i)
        elif (left_index < len(self.heap) and k > self.heap[left_index][key]):
            self.heapifyDown(i)
        elif (right_index < len(self.heap) and k > self.heap[right_index][key]):
            self.heapifyDown(i)
        elif debug:
            print "It is an heap"
    # end



def run(graph, vertex):

    explored = [False for _ in xrange(graph.n)]
    res = [INF for _ in xrange(graph.n)]
    h = Heap(graph.n)

    for n in xrange(graph.n):
        if n == vertex:
            h.insert_key(vertex, 0)
        else:
            h.insert_key(n, INF)

    while not all(explored):
        nearest = h.extractMin()
        nearest_index = nearest[0]
        nearest_distance = nearest[1]

        res[nearest_index] = nearest_distance
        explored[nearest_index] = True

        neighbors = graph.enumerate(nearest_index)

        for n, w in neighbors:
            new_distance = nearest_distance + w
            if not explored[n] and new_distance < h.getKey(n):
                h.changeKey(n, new_distance)

    return res
