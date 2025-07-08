import os
import pandas as pd
import numpy as np

path_to_folder = '/datag/users/ctremblay'
above_2_ghz = []
not_above_2_ghz = []

print('Starting looking through files.')

for file in os.scandir(path_to_folder):
    if file.is_file() and file.name.endswith('.pkl') and file.name.startswith('Summer'):
        try:
            df = pd.read_pickle(file.path)
            if 'signal_frequency' in df.columns:
                if np.min(df['signal_frequency']) > 2000:
                    above_2_ghz.append(file.path)
                    print('-', end = '', flush=True)
                else:
                    not_above_2_ghz.append(file.path)
            else:
                pass
        except Exception as e:
            pass
print('')

with open('output.txt', "w") as output:
    output.write("Above 2 Gigahertz:\n")
    for path in above_2_ghz:
        output.write(f'{path}\n')
    output.write(f'Number of files: {len(above_2_ghz)}\n\n')

    output.write("Not above 2 Gigahertz:\n")
    for path in not_above_2_ghz:
        output.write(f'{path}\n')
    output.write(f'Number of files: {len(not_above_2_ghz)}\n')
