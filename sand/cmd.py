import argparse, timeit, random, uuid
from sand import bf, graph


_data_structures = {
    'matrix': graph.AdjMatrixGraph,
    'list': graph.AdjListGraph,
}


def _get_times(alg, p, w, ds, nos):
    def timeme(nov):
        def f():
            graph = _data_structures[ds](nov, p, w)
            alg(graph, random.randint(0, nov - 1))
        return f

    return [timeit.timeit(timeme(n), number=20) for n in nos]


def breadth_first(args):
    p = args.p
    ds = args.ds
    nos = args.steps

    return _get_times(bf.run, p, 1, ds, nos)

_algorithms = {
    'bf': breadth_first,
}


def main():
    parser = argparse.ArgumentParser(
        description=
        '''
            Client to run algorithms on graphs.
        '''
    )

    parser.add_argument('p', type=float, help='The probability for two edges to be connected')
    parser.add_argument('algorithm', help='The algorithm to run. Choose among: ' + ', '.join(_algorithms.keys()))
    parser.add_argument('-ds', '--data-structure', default='matrix', dest='ds',
            help='The data structure used to store the graph. Choose among: ' + ', '.join(_data_structures.keys()))
    parser.add_argument('--plot', default=False, action='store_true',
            help='Plot the results to plot.ly')
    parser.add_argument('--steps', type=int, nargs='+', default=list(xrange(100, 1100, 100)),
            help='The steps for which the algorithm will run')

    args = parser.parse_args()

    if not args.ds in _data_structures:
        print ds + ' is not in the data structures:'
        print _data_structures.keys()
        return 1

    if not args.algorithm in _algorithms:
        print args.algorithm + ' is not in the data structures:'
        print _algorithms.keys()
        return 1

    times = _algorithms[args.algorithm](args)
    steps = args.steps

    if args.plot:
        import plotly.plotly as ply

        data = [dict(x=steps, y=times)]
        fname = str(uuid.uuid1())[:8]
        print ply.plot(data, filename=fname, auto_open=False)
    else:
        data = {steps[i]: times[i] for i in xrange(len(steps))}
        print data

    return 0

