#!/bin/bash

workloads=( a b c d e f )
#recordcounts=( 10000 100000 1000000 10000000 )
recordcounts=( 1000 10000 100000 1000000 )

read -p "Delete previous benchmark logs? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -r benchmark-output/*
fi

cd YCSB

echo -e ">> \e[31m- - - - - - - - - -\e[0m"
for i in "${workloads[@]}"
do
    for j in "${recordcounts[@]}"
    do
        echo -e ">> \e[101mRunnung workload $i with recordcount $j\e[0m:"
        echo -e ">> Starting at: $(date)"
        now=$(date +"%b%d-%Y-%H%M%S")
        docker exec aerospike aql -c "TRUNCATE test"
        echo -e ">> \e[41mSleeping ...\e[0m"
        sleep 5
        echo -e ">> \e[43mInserting data\e[0m"
        ./bin/ycsb load aerospike -P workloads/workload$i -P ../overwrite.dat -p as.namespace=test -p recordcount=$j -s >../benchmark-output/outputLoad-$i-$j.log || break 2;
        echo -e ">> \e[42mRunning benchmark\e[0m"
        ./bin/ycsb run aerospike -P workloads/workload$i -P ../overwrite.dat -p as.namespace=test -p recordcount=$j -s >../benchmark-output/outputRun-$i-$j.log || break 2;
        echo -e ">> \e[31m- - - - - - - - - -\e[0m"
    done
done

cd ..
