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

    def __init__(self, graph, pos):
        self.graph = graph
        self.active = True
        self.pos = pos

    def next(self):
        if random.random() > self.p_move:
            self.active = False

        if not self.active:
            return

        next_pos = random.choice(self.graph[self.pos])
        self.pos = next_pos


def main():
    csv_file = conf.get('output')
    times = int(conf.get('no_iterations'))
    no_epochs = int(conf.get('no_epochs'))

    graph = _load_adjlist(csv_file)

    x = {auth: 1 - Crawler.p_move for auth in graph.keys()}
    for _ in xrange(times):
        crawlers = []

        # run epochs
        for _ in xrange(no_epochs):
            # generate 1 - d crawlers
            crawlers.extend(
                [Crawler(graph, pos) for pos in graph.keys()
                    if random.random() > Crawler.p_move]
            )
            for crawler in crawlers:
                crawler.next()

        for crawler in crawlers:
            if crawler.active:
                x[crawler.pos] += 1

    # compute the average and normalize
    x = {auth: float(rank) / times / len(graph)
            for auth, rank in x.iteritems()}

    ranking = x.keys()
    ranking.sort(key=x.get, reverse=True)

    fname = 'stochastic.out'
    with open(fname, 'w') as f:
        for auth in ranking:
            f.write(str(auth) + ': ' + str(x[auth]) + '\n')

    print
    print 'You can find the complete crawling output in {}'.format(fname)
