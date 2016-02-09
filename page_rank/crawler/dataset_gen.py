import urllib2
from lxml import html
from crawler import config as conf

_OUTPUT_FILE = conf.get('output')
_BASE_URL = conf.get('base_url')
_START_URL = conf.get('start_author_url')
_START_LABEL = conf.get('start_author_label')
_NO_VERTICES = int(conf.get('no_vertices'))
_YEAR = conf.get('year')

_base_query = '//tr[td[2][text() >= ' + _YEAR + ']]/td[3]//*[a[1][text() = "{}"]]/a[position()>1][@class = "authority author"]/'
_labels_query = _base_query + 'text()'
_hrefs_query = _base_query + '@href'


def main():
    adjmatrix = [[0]]
    labels = {_START_LABEL: 0}
    urls = {_START_LABEL: _START_URL}
    explored = set()
    last_explored_count = -1

    def update_labels(label):
        new_vertex = max(labels.values()) + 1
        labels[label] = new_vertex

    def update_matrix():
        for row in adjmatrix:
            row.append(0)

        adjmatrix.append([0 for _ in xrange(len(adjmatrix[0]))])

    def add_edge(i, j):
        adjmatrix[i][j] = 1

    def get_authors(url, label):
        page_content = urllib2.urlopen(url).read()
        dom = html.fromstring(page_content)
        labs = dom.xpath(_labels_query.format(label))
        hrefs = dom.xpath(_hrefs_query.format(label))

        return {labs[i]: hrefs[i] for i in xrange(len(labs))}

    while last_explored_count < len(explored) and \
            len(adjmatrix) < _NO_VERTICES:
        last_explored_count = len(explored)
        print 'The number of vertices now is {}'.format(last_explored_count)
        next_urls = {}

        for label, url in urls.iteritems():
            if label not in explored:
                print 'Examining {}...'.format(label)
                explored.add(label)
                coauthors = get_authors(_BASE_URL + url, label)

                for author in coauthors:
                    if author not in labels:
                        # found a new node
                        update_labels(author)
                        update_matrix()
                    add_edge(labels[author], labels[label])

                next_urls.update(coauthors)

        urls = next_urls

    print
    print 'Stopped at {} nodes'.format(len(adjmatrix))

    def prettify(label):
        return label.replace(',', '').replace(' ', '_')

    labs = labels.keys()
    labs.sort(key=labels.get)
    labs = map(prettify, labs)

    # to csv file
    with open(_OUTPUT_FILE, 'w') as f:
        for v, row in enumerate(adjmatrix):
            neighs = [i for i in xrange(len(row)) if row[i] == 1]
            neighs = [labs[i] for i in neighs]
            neighs.insert(0, labs[v])
            f.write(','.join([str(el) for el in neighs]) + '\n')

    print
    print 'Output written to {}'.format(_OUTPUT_FILE)
