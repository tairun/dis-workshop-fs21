#!/bin/bash

AEROSPIKE_CONF=/opt/aerospike/etc/aerospike-hybrid_4G-rf_1.conf
#AEROSPIKE_CONF=/opt/aerospike/etc/aerospike-disk_4G-rf_1.conf
#AEROSPIKE_CONF=/opt/aerospike/etc/aerospike-mem_4G-rf_1.conf

#workloads=( a b c d e f )
workloads=( a b c d  f )
#recordcounts=( 1000 10000 100000 1000000 10000000 )
recordcounts=( 10000 100000 1000000 )

read -p "Confirm delete previous benchmark logs? [yY]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -r benchmark-output/*
    docker stop aerospike && docker rm aerospike
fi

echo -e ">> \e[31m  - - - - - - - - - -  \e[0m"
for i in "${workloads[@]}"
do
    for j in "${recordcounts[@]}"
    do
        echo -e ">> \e[101m  Runnung workload $i with recordcount $j  \e[0m:"
        echo -e ">> Starting at: $(date)"
        now=$(date +"%b%d-%Y-%H%M%S")
        
        ## Reset database to emtpy state:
        ## Either use TRUNCATE or restart container
        
        #docker exec aerospike aql -c "TRUNCATE test"
        docker stop aerospike && docker rm aerospike
        docker run -d -v "$(pwd)/confs/:/opt/aerospike/etc/" --name aerospike -p 3000-3002:3000-3002 aerospike/aerospike-server --config-file $AEROSPIKE_CONF

        ## Lets wait for docker run to its thing
        echo -e ">> \e[41m  Sleeping ...\e[0m"
        sleep 5

        cd YCSB
        echo -e ">> \e[43m  Inserting data  \e[0m"
        ./bin/ycsb load aerospike -P workloads/workload$i -P ../overwrite.dat -p as.namespace=test -p recordcount=$j -s >../benchmark-output/outputLoad-$i-$j.log || break 2;
        echo -e ">> \e[42m  Running benchmark  \e[0m"
        ./bin/ycsb run aerospike -P workloads/workload$i -P ../overwrite.dat -p as.namespace=test -p operationcount=$j -s >../benchmark-output/outputRun-$i-$j.log || break 2;
        echo -e ">> \e[31m  - - - - - - - - - -  \e[0m"
        cd ..
    done
done

echo -e "\e[33mI think we're done here! Bye.\e[0m"