#!/usr/bin/env python

import pprint
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from typing import List, Dict


def load_file_content(filename: str) -> List[str]:
    with open(filename, mode='r', encoding='utf-8') as log:
        return log.readlines()


def parse_load_log(log: List[str]) -> Dict:
    load_data = dict()

    for i, elem in enumerate(log):
        if '[INSERT], Return=OK' in elem:
            start_index = i+1
            break

    match_runtime = [match for match in log if 'RunTime(ms)' in match]
    match_ops = [match for match in log if 'Throughput(ops/sec)' in match]
    match_insert_ops = [match for match in log if '[INSERT], Operations' in match]
    match_insert_avg = [match for match in log if '[INSERT], AverageLatency(us)' in match]
    match_insert_min = [match for match in log if '[INSERT], MinLatency(us)' in match]
    match_insert_max = [match for match in log if '[INSERT], MaxLatency(us)' in match]
    match_insert_timeseries = [match for match in log[start_index:] if '[INSERT]' in match]

    load_data['runtime'] = int(match_runtime[0].split(',')[2].strip())
    load_data['throughput'] = round(float(match_ops[0].split(',')[2].strip()), 2)
    load_data['ops'] = int(match_insert_ops[0].split(',')[2].strip())
    load_data['ops_avg'] = round(float(match_insert_avg[0].split(',')[2].strip()), 2)
    load_data['ops_min'] = round(float(match_insert_min[0].split(',')[2].strip()), 2)
    load_data['ops_max'] = round(float(match_insert_max[0].split(',')[2].strip()), 2)
    load_data['insert_x'] = [int(x.split(',')[1].strip()) for x in match_insert_timeseries]
    load_data['insert_y'] = [round(float(y.split(',')[2].strip()), 2) for y in match_insert_timeseries]

    return load_data


def parse_run_log(log: List[str]) -> Dict:
    run_data = dict()

    for i, elem in enumerate(log):
        if '[INSERT], Return=OK' in elem:
            start_insert_index = i+1
            break
        else:
            start_insert_index = None

    for i, elem in enumerate(log):
        if '[READ], Return=OK' in elem:
            start_read_index = i+1
            break
        else:
            start_read_index = None

    for i, elem in enumerate(log):
        if '[UPDATE], Return=OK' in elem:
            start_update_index = i+1
            break
        else:
            start_update_index = None

    match_runtime = [match for match in log if 'RunTime(ms)' in match]
    match_ops = [match for match in log if 'Throughput(ops/sec)' in match]
    run_data['runtime'] = int(match_runtime[0].split(',')[2].strip())
    run_data['throughput'] = round(float(match_ops[0].split(',')[2].strip()), 2)

    if start_insert_index:
        match_insert_ops = [match for match in log if '[INSERT], Operations' in match]
        match_insert_avg = [match for match in log if '[INSERT], AverageLatency(us)' in match]
        match_insert_min = [match for match in log if '[INSERT], MinLatency(us)' in match]
        match_insert_max = [match for match in log if '[INSERT], MaxLatency(us)' in match]
        match_insert_timeseries = [match for match in log[start_insert_index:] if '[INSERT]' in match]
        run_data['insert']['ops'] = int(match_insert_ops[0].split(',')[2].strip())
        run_data['insert']['ops_avg'] = round(float(match_insert_avg[0].split(',')[2].strip()), 2)
        run_data['insert']['ops_min'] = round(float(match_insert_min[0].split(',')[2].strip()), 2)
        run_data['insert']['ops_max'] = round(float(match_insert_max[0].split(',')[2].strip()), 2)
        run_data['insert']['x'] = [int(x.split(',')[1].strip()) for x in match_insert_timeseries]
        run_data['insert']['y'] = [round(float(y.split(',')[2].strip()), 2) for y in match_insert_timeseries]

    if start_read_index:
        match_read_ops = [match for match in log if '[READ], Operations' in match]
        match_read_avg = [match for match in log if '[READ], AverageLatency(us)' in match]
        match_read_min = [match for match in log if '[READ], MinLatency(us)' in match]
        match_read_max = [match for match in log if '[READ], MaxLatency(us)' in match]
        match_read_timeseries = [match for match in log[start_read_index:] if '[READ]' in match]
        # make empty dict with key 'read'
        run_data['read']['ops'] = int(match_read_ops[0].split(',')[2].strip())
        run_data['read']['ops_avg'] = round(float(match_read_avg[0].split(',')[2].strip()), 2)
        run_data['read']['ops_min'] = round(float(match_read_min[0].split(',')[2].strip()), 2)
        run_data['read']['ops_max'] = round(float(match_read_max[0].split(',')[2].strip()), 2)
        run_data['read']['x'] = [int(x.split(',')[1].strip()) for x in match_read_timeseries]
        run_data['read']['y'] = [round(float(y.split(',')[2].strip()), 2) for y in match_read_timeseries]

    if start_update_index:
        match_update_ops = [match for match in log if '[UPDATE], Operations' in match]
        match_update_avg = [match for match in log if '[UPDATE], AverageLatency(us)' in match]
        match_update_min = [match for match in log if '[UPDATE], MinLatency(us)' in match]
        match_update_max = [match for match in log if '[UPDATE], MaxLatency(us)' in match]
        match_update_timeseries = [match for match in log[start_update_index:] if '[UPDATE]' in match]
        run_data['update']['ops'] = int(match_update_ops[0].split(',')[2].strip())
        run_data['update']['ops_avg'] = round(float(match_update_avg[0].split(',')[2].strip()), 2)
        run_data['update']['ops_min'] = round(float(match_update_min[0].split(',')[2].strip()), 2)
        run_data['update']['ops_max'] = round(float(match_update_max[0].split(',')[2].strip()), 2)
        run_data['update']['x'] = [int(x.split(',')[1].strip()) for x in match_update_timeseries]
        run_data['update']['y'] = [round(float(y.split(',')[2].strip()), 2) for y in match_update_timeseries]

    return run_data


def plot_benchmark(load_list: List[str], run_list: List[str]) -> None:
    pass

    # Step through the sorted logfiles. The 
    for pair in zip(load_list, run_list):
        # Load the raw file contents from the file with ascending record count
        raw_load = load_file_content(pair[0])
        raw_run = load_file_content(pair[1])

        load_data = parse_load_log(raw_load)
        run_data = parse_run_log(raw_run)

       

        fig, axes = plt.subplots(nrows=len(load_list), ncols=2)
        st = fig.suptitle('Workload A', fontsize=16)
        
        axes[0][0].set_title('Load')
        axes[0][1].set_title('Run')

        for i in range(len(load_list)):
            load_index = np.arange(len(load_data['insert_x']))
            run_index = np.arange(len(run_data['insert']['x']))

            axes[i][0].bar(load_index, load_data['insert_y'])
            axes[i][0].set_xticklabels([''] + load_data['insert_x'])

            axes[i][0].bar(run_index, run_data['insert']['y'])
            axes[i][0].set_xticklabels([''] + run_data['insert']['x'])
            #ax1.set_xlabel('time (ms)')
            #ax1.set_ylabel('latency (us)')
            #ax2.set_title('records=100,000')

        plt.tight_layout()
        #st.set_y(0.95)
        # fig.subplots_adjust(top=0.80)
        # plt.text(0.2,0.9,f"RunTime(ms): {load_data['runtime']}" , transform=fig.transFigure)
        # plt.text(0.2,0.875,f"Throughput(ops/sec): {load_data['throughput']}" , transform=fig.transFigure)
        # plt.text(0.6,0.9,f"AverageLatency(us): {load_data['ops_avg']}" , transform=fig.transFigure)
        # plt.text(0.6,0.875,f"MinLatency(us): {load_data['ops_min']}" , transform=fig.transFigure)
        # plt.text(0.6,0.85,f"MaxLatency(us): {load_data['ops_max']}" , transform=fig.transFigure)
        plt.show()




if __name__ == '__main__':
    pp = pprint.PrettyPrinter(width=99, compact=False)

    run_types = ['Load', 'Run']
    workloads = ['a', 'b', 'c', 'd', 'e', 'f']

    basepath = './benchmark-output-copy'

    onlyfiles = [join(basepath, f) for f in listdir(basepath) if isfile(join(basepath, f))]

    workload_lists = [[file for file in onlyfiles if f"-{workload}-" in file] for workload in workloads]

    #pp.pprint(workload_lists)

    # Step through the list of workloads, then we filter to split by
    # load and run log. We call the plot_benchmark() function with the
    # two lists which generates a *.png file.
    for i, sublist in enumerate(workload_lists):
            load_list = list(filter(lambda name: 'Load' in name, sublist))
            run_list = list(filter(lambda name: 'Run' in name, sublist))
            
            #pp.pprint(load_list)
            #pp.pprint(run_list)

            plot_benchmark(load_list, run_list)
            pause = input('THIS IS WORKLOAD A')

""" file1 = './benchmark-output-copy/outputLoad-a-10000.log'
file2 = './benchmark-output-copy/outputRun-a-10000.log'

with open(file1, mode='r', encoding='utf-8') as log:
    raw_load = log.readlines()

# pp.pprint(raw_load)

with open(file1, mode='r', encoding='utf-8') as log:
    raw_run = log.readlines()

# pp.pprint(raw_run)

load_data = dict()
run_data = dict()

for i, elem in enumerate(raw_load):
    if '[INSERT], Return=OK' in elem:
        start_index = i+1
        break

match_runtime = [match for match in raw_load if 'RunTime(ms)' in match]
match_ops = [match for match in raw_load if 'Throughput(ops/sec)' in match]
match_insert_ops = [match for match in raw_load if '[INSERT], Operations' in match]
match_insert_avg = [match for match in raw_load if '[INSERT], AverageLatency(us)' in match]
match_insert_min = [match for match in raw_load if '[INSERT], MinLatency(us)' in match]
match_insert_max = [match for match in raw_load if '[INSERT], MaxLatency(us)' in match]
match_insert_timeseries = [match for match in raw_load[start_index:] if '[INSERT]' in match]

load_data['runtime'] = int(match_runtime[0].split(',')[2].strip())
load_data['throughput'] = round(float(match_ops[0].split(',')[2].strip()), 2)
load_data['ops'] = int(match_insert_ops[0].split(',')[2].strip())
load_data['ops_avg'] = round(float(match_insert_avg[0].split(',')[2].strip()), 2)
load_data['ops_min'] = round(float(match_insert_min[0].split(',')[2].strip()), 2)
load_data['ops_max'] = round(float(match_insert_max[0].split(',')[2].strip()), 2)
load_data['insert_x'] = [int(x.split(',')[1].strip()) for x in match_insert_timeseries]
load_data['insert_y'] = [round(float(y.split(',')[2].strip()), 2) for y in match_insert_timeseries]

print(start_index)
pp.pprint(load_data)

index = np.arange(len(load_data['insert_x']))

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

st = fig.suptitle('Workload A', fontsize=16)
ax1.set_title('records=10,000')
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('latency (us)')
ax2.set_title('records=100,000')
ax1.bar(index, load_data['insert_y'])
ax1.set_xticklabels([''] + load_data['insert_x'])
ax2.bar(index, load_data['insert_y'])
ax3.bar(index, load_data['insert_y'])
ax4.bar(index, load_data['insert_y'])

plt.tight_layout()
#st.set_y(0.95)
fig.subplots_adjust(top=0.80)
plt.text(0.2,0.9,f"RunTime(ms): {load_data['runtime']}" , transform=fig.transFigure)
plt.text(0.2,0.875,f"Throughput(ops/sec): {load_data['throughput']}" , transform=fig.transFigure)
plt.text(0.6,0.9,f"AverageLatency(us): {load_data['ops_avg']}" , transform=fig.transFigure)
plt.text(0.6,0.875,f"MinLatency(us): {load_data['ops_min']}" , transform=fig.transFigure)
plt.text(0.6,0.85,f"MaxLatency(us): {load_data['ops_max']}" , transform=fig.transFigure)
plt.show() """