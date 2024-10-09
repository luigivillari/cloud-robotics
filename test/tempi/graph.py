# import pandas as pd
# import matplotlib.pyplot as plt


# df = pd.read_csv('test/tempi/timing_data_means_sorted.csv')


# plt.plot(df['avg_t3-t0'], marker='', linestyle='-', color='blue', linewidth=2, markersize=8)


# plt.xlabel('Numero dispositivi (120)', fontsize=12)
# plt.ylabel('Tempo (s)', fontsize=12)
# plt.title('Andamento dei tempi di esecuzione (10 iterazioni, 120 dispositivi)', fontsize=10, fontweight='bold')


# plt.grid(axis='y', linestyle='--', alpha=0.7)


# plt.tight_layout()
# plt.show()



# import pandas as pd
# import matplotlib.pyplot as plt


# #df = pd.read_csv('test/tempi/timing_data_means_sorted_fsm.csv') 
# df_2 = pd.read_csv('test/tempi/timing_data_means_sorted.csv') # Sostituisci con il percorso corretto del tuo file


# avg_t0_t1 = df_2['avg_t0-t1'].mean()
# avg_t1_t2 = df_2['avg_t1-t2'].mean()
# avg_t2_t3 = df_2['avg_t2-t3'].mean()
# avg_t3_t0 = df_2['avg_t3-t0'].mean()
# # avg_t0_t1 = df['avg_t0-t1_fsm'].mean()
# # avg_t1_t2 = df['avg_t1-t2_fsm'].mean()
# # avg_t2_t3 = df_2['avg_t2-t3'].mean()


# labels = ['t0-t1','t1-t2', 't2-t3','t3-t0']
# averages = [avg_t0_t1, avg_t1_t2, avg_t2_t3, avg_t3_t0]

# plt.figure(figsize=(10, 6))  # Imposta la dimensione della figura
# plt.bar(labels, averages, color=['blue', 'green', 'red','purple'])  # Aggiungi colori alle barre


# plt.ylabel('Tempo (s)', fontsize=12)
# plt.xlabel('Intervalli', fontsize=12)
# plt.title('Tempo medio per ogni intervallo (10 iterazioni, 120 dispositivi)', fontsize=14, fontweight='bold')


# plt.grid(axis='y', linestyle='--', alpha=0.7)


# plt.tight_layout()


# plt.show()


import pandas as pd
import matplotlib.pyplot as plt


df_2 = pd.read_csv('test/tempi/timing_data_means_sorted.csv')


sum_30 = df_2['avg_t3-t0'][:30].sum()
sum_70 = df_2['avg_t3-t0'][:70].sum()
sum_120 = df_2['avg_t3-t0'][:120].sum()
print(sum_120)


labels = ['30', '70', '120']
sums = [sum_30, sum_70, sum_120]


plt.figure(figsize=(10, 6)) 
plt.bar(labels, sums, color=['orange', 'orange', 'orange'],width=0.5) 


plt.ylabel('Tempo (s)', fontsize=12)
plt.xlabel('Numero di dispositivi', fontsize=12)
plt.title('Tempi di esecuzione totali per N dispositivi avviati (10 iterazioni)', fontsize=14, fontweight='bold')


plt.grid(axis='y', linestyle='--', alpha=0.7)


plt.tight_layout()


plt.show()
