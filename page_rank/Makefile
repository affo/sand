TEST_IMG=flink_pagerank
CNAME=pagerank-running
MAIN_CLASS=it.polimi.sand.PageRank
OPTS=

all: iterative stochastic

dataset:
	./bin/pagerank_dataset_gen

it_clean:
	docker rm -f $(CNAME); true

it_build:
	mvn clean install -Pbuild-jar
	docker build -t $(TEST_IMG) .

iterative: it_clean it_build
	docker run -it -p 48081:8081 --name $(CNAME) $(TEST_IMG) -c$(MAIN_CLASS) $(OPTS)
	docker cp $(CNAME):/iterative.out .
	# you can see PageRank output at iterative.out file

stochastic:
	./bin/pagerank_launch_crawlers
