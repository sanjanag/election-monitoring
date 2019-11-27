import glob

import matplotlib.pyplot as plt
import pandas as pd

csv_files = glob.glob("./logs/ranked-list*")
csv_files.sort()

# concatenate batches
K = 1000
df_list = []
fields = ['Text', 'timestamp', 'status', 'rank_score', 'incident_category']
for i, f in enumerate(csv_files):
    df = pd.read_csv(f, usecols=fields).head(K)
    df['batch'] = i + 1
    df_list.append(df)
df = pd.concat(df_list)

# get counts
df = df.groupby(['batch', 'incident_category']).size().reset_index(
    name='counts')
df_count = df.pivot_table('counts', ['batch'], 'incident_category',
                          fill_value=0)
df_count = df_count.drop(columns=['Others'])

# plot
df_count.plot(kind='barh', stacked=True, figsize=(10, 7))
plt.title("Category count for first 1000 tweets in each ranked batch")
plt.xlabel("Count")
plt.savefig(f'category_{K}.png')
