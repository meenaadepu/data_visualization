import matplotlib.pyplot as plt
import pandas as pd
from textwrap import wrap
import seaborn as sns
out_path = "D:\Meena\Automation\plots\DPHY\outputs"

df = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet1")
df_ref = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet2")
cols = list(df.columns)
df.columns = cols
fcols = cols[6:]
print(fcols)
medianprops = dict(color='red', linewidth=5 )
for k, col in enumerate(fcols):
    print(col)
    f1 = plt.figure(figsize=(12, 7))
    ax1 = f1.add_subplot(111)
    Spec_Min = float((df_ref[col][0:1]))
    Spec_Max = float((df_ref[col][1:2]))
    units = df_ref[col][2:3].values
    Median = df[col].median()

  #  df.boxplot(column=col, vert=0,return_type='axes',ax=ax1,medianprops=medianprops,widths=0.4,patch_artist=True,)
    bp = ax1.boxplot(df[col],vert =0,widths=0.5, patch_artist=True)
    for median in bp['medians']:
        median.set(color='k', linewidth=1, )
        x, y = median.get_data()
        xn = (x - (x.sum() / 2.)) * 0.5 + (x.sum() / 2.)
        ax1.plot(xn, y, color="k", linewidth=5, solid_capstyle="butt", zorder=4)

    ax1.axvline(x=Spec_Min, linestyle='-.', color='g', label="Spec_Min")
    ax1.axvline(x=Spec_Max, linestyle='-.', color='r', label="Spec_Max")
    ax1.axvline(x=Median, linestyle='--', color='b', label="Median")


    ax1.xaxis.set_tick_params(rotation=70, labelsize=10,)
    ax1.set_xlabel(str(units), size=12.5, fontdict=dict(weight='bold'), labelpad=10)
    ax1.set_title(col, size=16, y=1.02, fontdict=dict(weight='bold'))
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), fancybox=False, shadow=False, ncol=10, edgecolor='black',prop={'size': 12})

    for axis in ['top', 'bottom', 'left', 'right']:
        ax1.spines[axis].set_linewidth(2)
        ax1.spines[axis].set_color("black")
        ax1.spines[axis].set_zorder(0)

   # plt.show()
    f1_outpath = out_path+"\\" +str(k)+"single"+ col[0:10].replace(":","_") + ".png"
    f1.savefig(f1_outpath, bbox_inches='tight')
    plt.cla()


