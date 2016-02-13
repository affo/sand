def run(graph, vertex):
    res = [-1 for _ in xrange(graph.n)]
    res[vertex] = 0
    current_distance = 0

    while any([v < 0 for v in res]):
        to_explore = [ i for i in xrange(graph.n) if res[i] == current_distance ]
        neighbors = []
        
        for v in to_explore:
            local_neighbors = graph.enumerate(v)
            for n, c in local_neighbors:
                if n not in neighbors:
                    neighbors.append(n)

        for n in neighbors:
            if res[n] == -1:
                res[n] = current_distance + 1

        current_distance = current_distance + 1

    return res
