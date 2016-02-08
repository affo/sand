#!/bin/bash
start-local.sh
flink run "$@" pagerank.jar
