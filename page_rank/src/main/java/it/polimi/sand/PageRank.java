package it.polimi.sand;

import org.apache.flink.api.java.ExecutionEnvironment;

public class PageRank {

    public static void main(String[] args) throws Exception {

        // set up the execution environment
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        System.out.println(env.getId() + " - Hello from Flink!");

    }
}
