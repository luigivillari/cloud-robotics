import os
import re
import csv


log_directory = './logs_fsm' 


csv_file = 'timing_fsm.csv'


fsm_pattern = re.compile(r"t(\d)-t(\d)-fsm:\s*([\d.]+)")  # Trova pattern tipo "t0-t1_fsm: 0.015"


log_data = []


for log_file in os.listdir(log_directory):
    if log_file.endswith('.log'):
        # Estrai l'ID del container dal nome del file (es. log_1001.log -> ID=1001)
        container_id = log_file.split('_')[1].split('.')[0] 
        line_counter = 0
        t0_t1_fsm, t1_t2_fsm = None, None

        with open(os.path.join(log_directory, log_file), 'r') as file:
            for line in file:
           
                match = fsm_pattern.search(line)
                if match:
                  
                    t_start = match.group(1)
                    t_end = match.group(2)
                    time_value = float(match.group(3))

              
                    if t_start == "0" and t_end == "1":
                        t0_t1_fsm = time_value
                    elif t_start == "1" and t_end == "2":
                        t1_t2_fsm = time_value

                  
                    if t0_t1_fsm is not None and t1_t2_fsm is not None:
                        log_data.append([container_id, t0_t1_fsm, t1_t2_fsm])
                        line_counter += 1  

                       
                        t0_t1_fsm, t1_t2_fsm = None, None

                 
                    if line_counter >= 10:
                        break


log_data.sort(key=lambda x: int(x[0]))


with open(csv_file, mode='w', newline='') as csv_output:
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(['ID', 't0-t1_fsm', 't1-t2_fsm'])
    csv_writer.writerows(log_data)

print(f"Dati salvati in {csv_file}")
