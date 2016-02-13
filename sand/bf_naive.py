def run(graph, vertex):
    res = [-1 for _ in xrange(graph.n)]
    res[vertex] = 0
    current_distance = 0

    while any([v < 0 for v in res]):
        new_layer = [ i for i in xrange(graph.n) if res[i] == current_distance ]
        all_neighbors = []
        
        for next_vertex in new_layer:
            neighbors = graph.enumerate(next_vertex)
            for v in neighbors:
                all_neighbors.append(v[0])

        if all_neighbors == []:
            return res

        for n in all_neighbors:            
            if res[n] == -1:
                res[n] = current_distance + 1

        current_distance = current_distance + 1

    return res
