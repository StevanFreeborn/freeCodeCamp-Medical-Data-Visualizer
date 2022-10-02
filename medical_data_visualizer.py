import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./medical_examination.csv')

df['overweight'] = df['overweight'] = (df['weight'] / ((df['height'] * 0.01) ** 2)) > 25

df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

def draw_cat_plot():
  value_vars = sorted(['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
  df_cat = pd.melt(df, id_vars=['cardio'], value_vars=value_vars)
  plot = sns.catplot(x='variable', col='cardio', hue='value', kind='count', data=df_cat).set_axis_labels('variable', 'total')
  fig = plot.fig
  fig.savefig('catplot.png')
  return fig

def draw_heat_map():
  df_heat = df[
    (df['ap_lo'] <= df['ap_hi']) & 
    (df['height'] >= df['height'].quantile(0.025)) &
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975))
    ]

  corr = df_heat.corr()
  mask = np.triu(np.ones_like(corr))
  fig, ax = plt.subplots(figsize=(10,10))
  sns.heatmap(corr, vmin=0, vmax=0.25, annot=True, fmt='.1f', linewidths=0, square=True, mask=mask)
  fig.savefig('heatmap.png')
  return fig
