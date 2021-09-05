import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
import pandas as pd
import math
import matplotlib.pyplot as plt

def plot_heatmap(in_file, out_file, title_str, cmap):
    heatmap_dat = pd.read_csv(in_file)

    # read concentration from string formatted as e.g. '[.0001]'
    heatmap_dat['Concentration B (M)'] = heatmap_dat['Concentration B (M)'] \
            .map(lambda x: x[1:-1]).astype('float').round(3)

    # drop empty cols
    heatmap_dat.drop(heatmap_dat.columns[[-1,-2]], axis=1, inplace=True)

    # group by each square in the final heatmap and apply max/min/mean
    heatmap_dat = heatmap_dat.groupby(['Concentration B (M)', 'Antisolvent']) \
            .max().reset_index()

    # pivot to heatmap friendly (cols as antisolvent, rows as concentration)
    heatmap_dat = heatmap_dat.pivot(index='Concentration B (M)', 
            columns='Antisolvent',
            values='Intensity')

    # heatmap
    xticks = np.linspace(0,1,6)
    ax = sns.heatmap(heatmap_dat.transpose(),
            cmap = cmap,
            cbar_kws={'label': 'Intensity (counts)'})
    locs, labels = plt.xticks()

    ax.set_xticks([0,5,10,15,20])
    ax.set_xticklabels(['0','0.25','0.5','0.75','1'])

    plt.title("PL Intensity heatmap for {}".format(title_str))

    plt.xticks(rotation=0)
    plt.savefig(out_file, dpi=150)
    plt.clf()

plot_heatmap('data/PEABr_antisolvent_heatmap_9_3.csv',
        'figs/heatmap_(PEABr)2-PbBr2.png',
        '$(PEABr)_{2}-PbBr_{2}$',
        'Blues')
plot_heatmap('data/20210608-(4MeOPEAI)2-PbI2 - rough.csv',
        'figs/heatmap_(MeOPEAI)2-PbI2.png',
        '$(MeOPEAI)_{2}-PbI_{2}$',
        'Greens')
