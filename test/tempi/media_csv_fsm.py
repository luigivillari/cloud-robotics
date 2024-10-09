import csv
from collections import defaultdict


input_csv = 'timing_fsm.csv'

output_csv = 'timing_data_means_sorted_fsm.csv'


data = defaultdict(lambda: {'t0_t1_fsm': [], 't1_t2_fsm': []})


with open(input_csv, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        
        device_id = row['ID']
        data[device_id]['t0_t1_fsm'].append(float(row['t0-t1_fsm']))
        data[device_id]['t1_t2_fsm'].append(float(row['t1-t2_fsm']))


averages = []
for device_id, times in data.items():
    avg_t0_t1_fsm = sum(times['t0_t1_fsm']) / len(times['t0_t1_fsm'])
    avg_t1_t2_fsm = sum(times['t1_t2_fsm']) / len(times['t1_t2_fsm'])
    averages.append([device_id, avg_t0_t1_fsm, avg_t1_t2_fsm])


averages.sort(key=lambda x: int(x[0]), reverse=True)


with open(output_csv, mode='w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
   
    csv_writer.writerow(['ID', 'avg_t0-t1_fsm', 'avg_t1-t2_fsm'])

    csv_writer.writerows(averages)

print(f"Dati medi salvati in {output_csv}")
