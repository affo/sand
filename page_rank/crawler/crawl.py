import random
from crawler import config as conf

def _load_adjlist(csv):
    al = {}
    with open(csv, 'r') as f:
        for line in f:
            line = line.strip()
            vertices = line.split(',')
            first_auth = vertices[0]
            coauths = vertices[1:]
            al[first_auth] = coauths

    return al


class Crawler(object):
    p_move = float(conf.get('p_follow_link'))

    def __init__(self, graph):
        self.graph = graph
        self.stopped = False
        # starting position is random
        self.pos = random.choice(graph.keys())

    def next(self):
        if random.random() > self.p_move:
            self.stopped = True

        if self.stopped:
            return

        next_pos = random.choice(self.graph[self.pos])
        self.pos = next_pos


def main():
    csv_file = conf.get('output')
    no_crawlers = int(conf.get('no_crawlers'))
    times = 100
    no_epochs = 50

    graph = _load_adjlist(csv_file)

    x = {auth: -1 for auth in graph.keys()}
    for _ in xrange(times):
        # generate crawlers
        crawlers = [Crawler(graph) for _ in xrange(no_crawlers)]

        # run epochs
        for _ in xrange(no_epochs):
            for crawler in crawlers:
                crawler.next()

        for crawler in crawlers:
            x[crawler.pos] += 1

    # compute the average and normalize
    x = {auth: float(rank) / times / no_crawlers
            for auth, rank in x.iteritems()}

    ranking = x.keys()
    ranking.sort(key=x.get, reverse=True)

    fname = 'stochastic.out'
    with open(fname, 'w') as f:
        for auth in ranking:
            f.write(str(auth) + ': ' + str(x[auth]) + '\n')

    print
    print 'You can find the complete crawling output in {}'.format(fname)
