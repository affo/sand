TEST_IMG=flink_pagerank
CNAME=pagerank-running
MAIN_CLASS=it.polimi.sand.PageRank
OPTS=

all: run

build:
	mvn clean install -Pbuild-jar
	docker build -t $(TEST_IMG) .

run: clean build
	docker run -it -p 48081:8081 --name $(CNAME) $(TEST_IMG) -c$(MAIN_CLASS) $(OPTS)

clean:
	docker rm -f $(CNAME); true
