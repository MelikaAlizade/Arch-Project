import subprocess
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def charts(label,metric,df1,df2,df3,df4):
    categories = ['LFURP', 'FIFORP', 'LRURP', 'MRURP']
    percentages = [df1['Value'][0],df2['Value'][0],df3['Value'][0],df4['Value'][0]]
    plt.bar(categories, percentages, color=['blue', 'orange', 'green', 'red'])
    plt.ylim(min(percentages)-0.05,max(percentages)+0.05)
    plt.yticks(np.arange(min(percentages)+0.05, max(percentages)+0.05, 0.05))
    plt.xlabel('Policies')
    plt.ylabel('CPI')
    plt.title(label)
    plt.savefig(f'{metric}.png')
    plt.show()

def charts2(label,metric,df1,df2,df3,df4):
    categories = ['LFURP', 'FIFORP', 'LRURP', 'MRURP']
    percentages = [df1['Value'][1],df2['Value'][1],df3['Value'][1],df4['Value'][1]]
    plt.bar(categories, percentages, color=['blue', 'orange', 'green', 'red'])
    plt.ylim(min(percentages)-500000,max(percentages)+500000)
    plt.yticks(np.arange(min(percentages)+500000, max(percentages)+500000, 500000))
    plt.xlabel('Policies')
    plt.ylabel('MissLatency')
    plt.title(label)
    plt.savefig(f'{metric}.png')
    plt.show()



def compile_c_program(source_file, output_file):
    try:
        # Run the gcc command
        subprocess.run(['gcc', '-o', output_file, source_file], check=True)
        print(f"Compilation successful. Binary created at {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")

def run_gem5_simulation(binary_file, repl_policy, test_number):
    try:
        # Construct the gem5 command
        gem5_command = [
            './build/X86/gem5.opt', 'configs/deprecated/example/se.py',
            '-c', binary_file,
            '--caches', '--l2cache',
            '--l2_size=4kB',
            '--mem-type=DDR4_2400_16x4',
            '--cacheline_size', '128',
            '--cpu-type=TimingSimpleCPU',
            f'--l2_repl={repl_policy}'
        ]
        
        print(f"Running gem5 command: {' '.join(gem5_command)}")
        
        # Run the gem5 command
        result = subprocess.run(gem5_command, check=True, capture_output=True, text=True)
        
        print(f"Simulation successful for {binary_file} with replacement policy {repl_policy}")
        print(f"Output: {result.stdout}")
        print(f"Errors: {result.stderr}")
        
        # Rename the stats.txt file
        stats_file = 'm5out/stats.txt'
        new_stats_file = f'm5out/stats_test{test_number}_{repl_policy}.txt'
        if os.path.exists(stats_file):
            os.rename(stats_file, new_stats_file)
            print(f"Renamed {stats_file} to {new_stats_file}")
            return new_stats_file
        else:
            print(f"{stats_file} does not exist")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed for {binary_file} with replacement policy {repl_policy}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Errors: {e.stderr}")
        return None

def extract_stats(stats_file):
    stats = {}
    if stats_file and os.path.exists(stats_file):
        with open(stats_file, 'r') as file:
            for line in file:
                if 'system.cpu.cpi' in line:
                    stats['system.cpu.cpi'] = float(line.split()[1])
                elif 'system.cpu.dcache.demandMissLatency::total' in line:
                    stats['system.cpu.dcache.demandMissLatency::total'] = float(line.split()[1])
    return stats

def save_stats_to_csv(stats, test_number, repl_policy):
    # Create the csvFiles directory if it doesn't exist
    if not os.path.exists('csvFiles'):
        os.makedirs('csvFiles')
    
    csv_file = f'csvFiles/csv{test_number}{repl_policy}.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metric', 'Value'])
        for key, value in stats.items():
            writer.writerow([key, value])
    print(f"Saved stats to {csv_file}")

replacement_policies = ['LRURP', 'FIFORP', 'LFURP', 'MRURP']

import concurrent.futures

def process_file(i):
    source_file = f'tests/New folder/test{i}.c'
    output_file = f'tests/New folder/test{i}'
    compile_c_program(source_file, output_file)
    
    for repl_policy in replacement_policies:
        stats_file = run_gem5_simulation(output_file, repl_policy, i)
        stats = extract_stats(stats_file)
        save_stats_to_csv(stats, i, repl_policy)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_file, range(1, 11))


#test1
csv_file1 = 'csv1LFURP.csv'
csv_file2 = 'csv1FIFORP.csv'
csv_file3 = 'csv1LRURP.csv'
csv_file4 = 'csv1MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test1","csv1CPI",df1,df2,df3,df4)
charts2("Test1","csv1Miss",df1,df2,df3,df4)

#test2
csv_file1 = 'csv2LFURP.csv'
csv_file2 = 'csv2FIFORP.csv'
csv_file3 = 'csv2LRURP.csv'
csv_file4 = 'csv2MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test2","csv2CPI",df1,df2,df3,df4)
charts2("Test2","csv2Miss",df1,df2,df3,df4)

#test3
csv_file1 = 'csv3LFURP.csv'
csv_file2 = 'csv3FIFORP.csv'
csv_file3 = 'csv3LRURP.csv'
csv_file4 = 'csv3MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test3","csv3CPI",df1,df2,df3,df4)
charts2("Test3","csv3Miss",df1,df2,df3,df4)

#test4
csv_file1 = 'csv4LFURP.csv'
csv_file2 = 'csv4FIFORP.csv'
csv_file3 = 'csv4LRURP.csv'
csv_file4 = 'csv4MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test4","csv4CPI",df1,df2,df3,df4)
charts2("Test4","csv4Miss",df1,df2,df3,df4)

#test5
csv_file1 = 'csv5LFURP.csv'
csv_file2 = 'csv5FIFORP.csv'
csv_file3 = 'csv5LRURP.csv'
csv_file4 = 'csv5MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test5","csv5CPI",df1,df2,df3,df4)
charts2("Test5","csv5Miss",df1,df2,df3,df4)

#test6
csv_file1 = 'csv6LFURP.csv'
csv_file2 = 'csv6FIFORP.csv'
csv_file3 = 'csv6LRURP.csv'
csv_file4 = 'csv6MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test6","csv6CPI",df1,df2,df3,df4)
charts2("Test6","csv6Miss",df1,df2,df3,df4)

#test7
csv_file1 = 'csv7LFURP.csv'
csv_file2 = 'csv7FIFORP.csv'
csv_file3 = 'csv7LRURP.csv'
csv_file4 = 'csv7MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test7","csv7CPI",df1,df2,df3,df4)
charts2("Test7","csv7Miss",df1,df2,df3,df4)

#test8
csv_file1 = 'csv8LFURP.csv'
csv_file2 = 'csv8FIFORP.csv'
csv_file3 = 'csv8LRURP.csv'
csv_file4 = 'csv8MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test8","csv8CPI",df1,df2,df3,df4)
charts2("Test8","csv8Miss",df1,df2,df3,df4)

#test9
csv_file1 = 'csv9LFURP.csv'
csv_file2 = 'csv9FIFORP.csv'
csv_file3 = 'csv9LRURP.csv'
csv_file4 = 'csv9MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test9","csv9CPI",df1,df2,df3,df4)
charts2("Test9","csv9Miss",df1,df2,df3,df4)

#test10
csv_file1 = 'csv10LFURP.csv'
csv_file2 = 'csv10FIFORP.csv'
csv_file3 = 'csv10LRURP.csv'
csv_file4 = 'csv10MRURP.csv'
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)
df3 = pd.read_csv(csv_file3)
df4 = pd.read_csv(csv_file4)
charts("Test10","csv10CPI",df1,df2,df3,df4)
charts2("Test10","csv10Miss",df1,df2,df3,df4)