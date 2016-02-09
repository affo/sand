FROM affo/flink:0.10.0

ADD target/pagerank.jar $FLINK_HOME/lib/
ADD target/pagerank.jar ./
ADD flink-conf.yaml $FLINK_HOME/conf/flink-conf.yaml
ADD run.sh ./
ADD src/main/resources/dataset.csv /dataset.csv

ENTRYPOINT [ "./run.sh" ]
