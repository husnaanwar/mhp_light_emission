import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
import pandas as pd
import math
import matplotlib.pyplot as plt

# this script demonstrates heatmap plotting

def plot_heatmap(in_file, out_file, title_str, cmap,
        xtick_list = [0,5,10,15,20],
        xticklabs = ['0','0.25','0.5','0.75','1']):
    heatmap_dat = pd.read_csv(in_file)

    # read concentration from string formatted as e.g. '[.0001]'
    heatmap_dat['Concentration B (M)'] = heatmap_dat['Concentration B (M)'] \
            .astype('float').round(3)

    # group by each square in the final heatmap and apply max/min/mean
    #heatmap_dat = heatmap_dat \
    #        .groupby(['Concentration B (M)', 'Antisolvent']) \
    #        .max().reset_index()

    heatmap_dat['antisolvent_rank'] = heatmap_dat \
            .groupby(['Concentration B (M)', 'Antisolvent']) \
            .cumcount()+1
    heatmap_dat['Antisolvent'] = heatmap_dat['Antisolvent'] \
            + heatmap_dat['antisolvent_rank'].astype(str)

    # pivot to heatmap friendly (cols as antisolvent, rows as concentration)
    heatmap_dat = heatmap_dat.pivot(index='Concentration B (M)', 
            columns='Antisolvent',
            values='Intensity')

    # heatmap
    xticks = np.linspace(0,1,6)
    ax = sns.heatmap(heatmap_dat.transpose(),
            cmap = cmap,
            cbar_kws={'label': 'Intensity (counts)'})

    ax.set_xticks(xtick_list)
    ax.set_xticklabels(xticklabs)

    plt.title("PL Intensity heatmap for {}".format(title_str))

    plt.xticks(rotation=0)
    plt.savefig(out_file, dpi=150)
    plt.clf()

plot_heatmap('data/PEABr_antisolvent_heatmap_9_3.csv',
        'figs/heatmap_(PEABr)2-PbBr2.png',
        '$(PEABr)_{2}-PbBr_{2}$',
        'Blues')
plot_heatmap('data/20210608-(4MeOPEAI)2-PbI2 - rough.csv',
        'figs/heatmap_(MeOPEAI)2-PbI2_rough.png',
        '$(MeOPEAI)_{2}-PbI_{2}$',
        'Greens')
plot_heatmap('data/20210616-(4MeOPEAI)2-PbI2.csv',
        'figs/heatmap_(MeOPEAI)2-PbI2.png',
        '$(MeOPEAI)_{2}-PbI_{2}$',
        'Greens',
        xtick_list = [1,14],
        xticklabs = ['0.25','0.875'])
