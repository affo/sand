def run(graph, vertex):
    res = [-1 for _ in xrange(graph.n)]
    queue = []
    read_pointer = 0

    res[vertex] = 0
    queue.append(vertex)

    while any([v < 0 for v in res]):
        next_vertex = queue[read_pointer]
        read_pointer += 1
        d = res[next_vertex]

        neighbors = graph.enumerate(next_vertex)
        neighbors = [v[0] for v in neighbors]

        for n in neighbors:
            if res[n] == -1:
                res[n] = d + 1
                queue.append(n)

    return res
