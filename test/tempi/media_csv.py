import csv
from collections import defaultdict


input_csv = 'timing.csv'

output_csv = 'timing_data_means_sorted.csv'


data = defaultdict(lambda: {'t0_t1': [], 't1_t2': [], 't2_t3': [], 't3_t0': []})


with open(input_csv, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
       
        device_id = row['ID']
        data[device_id]['t0_t1'].append(float(row['t0-t1']))
        data[device_id]['t1_t2'].append(float(row['t1-t2']))
        data[device_id]['t2_t3'].append(float(row['t2-t3']))
        data[device_id]['t3_t0'].append(float(row['t3-t0']))


averages = []
for device_id, times in data.items():
    avg_t0_t1 = sum(times['t0_t1']) / len(times['t0_t1'])
    avg_t1_t2 = sum(times['t1_t2']) / len(times['t1_t2'])
    avg_t2_t3 = sum(times['t2_t3']) / len(times['t2_t3'])
    avg_t3_t0 = sum(times['t3_t0']) / len(times['t3_t0'])
    averages.append([device_id, avg_t0_t1, avg_t1_t2, avg_t2_t3, avg_t3_t0])


averages.sort(key=lambda x: int(x[0]), reverse=True)


with open(output_csv, mode='w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
  
    csv_writer.writerow(['ID', 'avg_t0-t1', 'avg_t1-t2', 'avg_t2-t3', 'avg_t3-t0'])
  
    csv_writer.writerows(averages)

print(f"Dati medi salvati in {output_csv}")
