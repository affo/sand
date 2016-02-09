/*
 * This file has been obtained editing the original copy at
 * https://github.com/apache/flink/blob/master/flink-examples
 *  /flink-examples-batch/src/main/java/org/apache/flink/examples/java/graph/PageRank.java
 * in the official repository of the Apache Flink project.
 */

package it.polimi.sand;

import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.functions.FunctionAnnotation.ForwardedFields;
import org.apache.flink.api.java.operators.IterativeDataSet;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.util.Collector;

import java.util.Arrays;

import static org.apache.flink.api.java.aggregation.Aggregations.SUM;

@SuppressWarnings("serial")
public class PageRank {
    private static String inputPath = "file:///dataset.csv";
    private static String outputPath = "file:///iterative.out";
    private static int numPages = 114;
    private static int maxIterations = 100;

    // DAMPENING_FACTOR should match p_follow_link in crawler.conf
    private static final double DAMPENING_FACTOR = 0.85;
    private static final double EPSILON = 0.0001;

    // *************************************************************************
    //     PROGRAM
    // *************************************************************************

    public static void main(String[] args) throws Exception {

        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        // get input data
        DataSet<Tuple2<String, String[]>> adjlist = getAdjList(env);
        DataSet<String> authors = adjlist.map(new MapFunction<Tuple2<String, String[]>, String>() {
            @Override
            public String map(Tuple2<String, String[]> row) throws Exception {
                return row.f0;
            }
        });

        // assign initial rank to pages
        DataSet<Tuple2<String, Double>> pagesWithRanks = authors.
                map(new RankAssigner((1.0d / numPages)));

        // set iterative data set
        IterativeDataSet<Tuple2<String, Double>> iteration = pagesWithRanks.iterate(maxIterations);

        DataSet<Tuple2<String, Double>> newRanks = iteration
                // join pages with outgoing edges and distribute rank
                .join(adjlist).where(0).equalTo(0).flatMap(new JoinVertexWithEdgesMatch())
                // collect and sum ranks
                .groupBy(0).aggregate(SUM, 1)
                // apply dampening factor
                .map(new Dampener(DAMPENING_FACTOR, numPages));

        DataSet<Tuple2<String, Double>> finalPageRanks = iteration.closeWith(
                newRanks,
                newRanks.join(iteration).where(0).equalTo(0)
                        // termination condition
                        .filter(new EpsilonFilter()));

        // emit result
        finalPageRanks.print();
        finalPageRanks.writeAsCsv(outputPath, "\n", ": ");
        // execute program
        env.execute("Basic Page Rank Example");
    }


    // *************************************************************************
    //     USER FUNCTIONS
    // *************************************************************************

    /**
     * A map function that assigns an initial rank to all pages.
     */
    public static final class RankAssigner implements MapFunction<String, Tuple2<String, Double>> {
        Tuple2<String, Double> outPageWithRank;

        public RankAssigner(double rank) {
            this.outPageWithRank = new Tuple2<>("", rank);
        }

        @Override
        public Tuple2<String, Double> map(String page) {
            outPageWithRank.f0 = page;
            return outPageWithRank;
        }
    }

    /**
     * Join function that distributes a fraction of a vertex's rank to all neighbors.
     */
    public static final class JoinVertexWithEdgesMatch implements FlatMapFunction<Tuple2<Tuple2<String, Double>, Tuple2<String, String[]>>, Tuple2<String, Double>> {

        @Override
        public void flatMap(Tuple2<Tuple2<String, Double>, Tuple2<String, String[]>> value, Collector<Tuple2<String, Double>> out) {
            String[] neighbors = value.f1.f1;
            double rank = value.f0.f1;
            double rankToDistribute = rank / ((double) neighbors.length);

            for (String neighbor : neighbors) {
                out.collect(new Tuple2<>(neighbor, rankToDistribute));
            }
        }
    }

    /**
     * The function that applies the page rank dampening formula
     */
    @ForwardedFields("0")
    public static final class Dampener implements MapFunction<Tuple2<String, Double>, Tuple2<String, Double>> {

        private final double dampening;
        private final double randomJump;

        public Dampener(double dampening, double numVertices) {
            this.dampening = dampening;
            this.randomJump = (1 - dampening) / numVertices;
        }

        @Override
        public Tuple2<String, Double> map(Tuple2<String, Double> value) {
            value.f1 = (value.f1 * dampening) + randomJump;
            return value;
        }
    }

    /**
     * Filter that filters vertices where the rank difference is below a threshold.
     */
    public static final class EpsilonFilter implements FilterFunction<Tuple2<Tuple2<String, Double>, Tuple2<String, Double>>> {

        @Override
        public boolean filter(Tuple2<Tuple2<String, Double>, Tuple2<String, Double>> value) {
            return Math.abs(value.f0.f1 - value.f1.f1) > EPSILON;
        }
    }

    // *************************************************************************
    //     UTIL METHODS
    // *************************************************************************

    private static DataSet<Tuple2<String, String[]>> getAdjList(ExecutionEnvironment env) {
        DataSet<String> text = env.readTextFile(inputPath);
        return text
                .map(new MapFunction<String, Tuple2<String, String[]>>() {
                    @Override
                    public Tuple2<String, String[]> map(String s) throws Exception {
                        String[] row = s.split(",");

                        return new Tuple2<>(row[0], Arrays.copyOfRange(row, 1, row.length));
                    }
                });
    }
}
