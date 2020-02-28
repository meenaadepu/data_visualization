import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from openpyxl import load_workbook
import numpy as np
import matplotlib.ticker as mticker
#sns.set(style='whitegrid')

folder = "pll405_plots"
inputpath = r"D:\Meena\Automation\ATV\2227\pll405\refout"
outpath = r"D:\Meena\Automation\ATV\2227\pll405\outputs"
out_path = os.path.join(outpath, folder)
# Spec_Max=0.01
# Spec_Min=-0.01
if not os.path.exists(out_path):
    os.makedirs(out_path)
df_total = pd.DataFrame()
color_dict = {'FF': '#2980B9', 'FS': 'green', 'SF': 'violet', 'SS': 'orange', 'TT': 'coral'}

for path, subdirs, files in os.walk(inputpath):
    for name in files:
        print(name)
        fname = (os.path.join(path, name))
        df = pd.read_csv(fname)
        df1 = df.rename(columns={"Offset Frequency (Hz)": "Offset Frequency (Hz)","Phase Noise (dBc/Hz)":str(name)[0:3]})
       # print(df1.head(5))
        df_total = pd.concat([df_total,df1],axis=1)
        df_total = df_total.loc[:, ~df_total.columns.duplicated()]
        df_total.to_csv("df_total.csv")
       # print(df_total.shape)
        cols= list(df_total.columns)[1:]
        f1 = plt.figure(figsize=(18, 7))
        for k,i  in enumerate(cols):
           ax1 = f1.add_subplot(111)
           g=sns.lineplot(data=df_total, x=df_total.iloc[:,0], y=i,ax=ax1,color = str(color_dict[i[0:2]]))
        Title = "Refout Clock Phase Noise across PVT "
        ax1.set_xlabel("Offset Frequency (Hz)", size=12.5, fontdict=dict(weight='bold'), labelpad=10)
        ax1.set_ylabel("Phase Noise (dBc/Hz)", size=12.5, fontdict=dict(weight='bold'), labelpad=10)
        g.set_xscale('log')
        ax1.set_title(Title, size=12.5, fontdict=dict(weight='bold'))
        # ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.19), fancybox=False, shadow=False, ncol=10,
        #            edgecolor='black', prop={'size': 12})
        for axis in ['top', 'bottom', 'left', 'right']:
            ax1.spines[axis].set_linewidth(2)
            ax1.spines[axis].set_color("black")
        plt.grid(True, which="both", ls="--", c='gray')
        locmin = mticker.LogLocator(base=10, subs=np.arange(0.1, 1, 0.1), numticks=10)
        g.xaxis.set_minor_locator(locmin)
        g.xaxis.set_minor_formatter(mticker.NullFormatter())

       # plt.show()
        f1_outpath = out_path + "\\" + Title + ".png"
        #print(f1_outpath)
        f1.savefig(f1_outpath, bbox_inches='tight')
        plt.cla()
#plt.show()

print("completed")





