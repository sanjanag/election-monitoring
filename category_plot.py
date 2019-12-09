import glob

import matplotlib.pyplot as plt
import pandas as pd

csv_files = glob.glob("./logs/ranked-list*")
csv_files.sort()

# concatenate batches
df_list = []
fields = ['Text', 'timestamp', 'status', 'rank_score', 'incident_category']
for i, f in enumerate(csv_files):
    df = pd.read_csv(f, usecols=fields)
    df['batch'] = i + 1
    df_list.append(df)
df = pd.concat(df_list)

# get counts
df = df.groupby(['batch', 'incident_category']).size().reset_index(
    name='counts')
df_count = df.pivot_table('counts', ['batch'], 'incident_category',
                          fill_value=0)
df_count = df_count.drop(columns=['Others'])

df_count = df_count[
    ['Ballot Snatching', 'Delayed Logistics', 'Election Irregularity', 'Fraud',
     'Results', 'Violence']]

# plot
df_count.plot(kind='bar', stacked=True, figsize=(10, 7))
plt.title("Count of categories across batches")
plt.ylabel("Count")
plt.xlabel("Batch Index")
plt.savefig('category_chart.png')
