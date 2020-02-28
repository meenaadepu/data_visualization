import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

#creating output folder path#
folder = "PHY_Tx_Protocol_tests_Final_plots"
outpath = "D:\Meena\Automation\plots\DPHY\outputs"
out_path = os.path.join(outpath, folder)
if not os.path.exists(out_path):
    os.makedirs(out_path)

sns.set_style("whitegrid")
df = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet1")
df_ref = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet2")
custom_order ={'SS': 0,'SF': 1,'TT': 2,'FS': 3, 'FF': 4 }
df = df.iloc[df['Corner'].map(custom_order).argsort()]

# list the columns for creating plots#
cols = list(df.columns)
df.columns = cols
fcols = cols[6:7]

df["name"] = df["Temp"].astype(str)+df["Voltage"].astype(str)+df["Corner"].astype(str)
color_dict = dict({ 'SS': 'orange','SF': 'violet','TT': 'crimson','FS': 'green', 'FF': '#2980B9' })
medianprops = dict(linestyle='--', linewidth=5, color='k')

for k ,col in enumerate(fcols):
    print(col)
    f1 = plt.figure(figsize=(18, 7))
    f2 = plt.figure(figsize=(12, 5))
    ax1 = f1.add_subplot(111)
    ax2 = f2.add_subplot(111)
    Spec_Min = float((df_ref[col][0:1]))
    Spec_Max = float((df_ref[col][1:2]))
    units =   df_ref[col][2:3].values
    Median = df[col].median()
    print(Spec_Min, Spec_Max,Median,units)



    # creating multiple boxplots w.r.t to temp,voltage,process#
    sns.boxplot(data=df, x='name', y=col, hue='Corner',hue_order=['SS','SF','TT','FS','FF'],palette=color_dict,ax=ax1,medianprops=medianprops,whis='range')
    Min = round(df[col].min(), 1)
    Max = round(df[col].max(), 1)
    print(Min, Max)
    ax1.axhline(y=Min, linestyle='--', color='k', label=Min)
    ax1.axhline(y=Max, linestyle='--', color='k', label=Max)
    ax1.text(0, Min, Min, va='center', ha="right", bbox=dict(facecolor="w", alpha=0.5),
             transform=ax1.get_yaxis_transform(), size=11.5, )
    ax1.text(0, Max, Max, va='center', ha="right", bbox=dict(facecolor="w", alpha=0.5),
             transform=ax1.get_yaxis_transform(), size=11.5, )
    ax1.axhline(y=Spec_Min, linestyle='-.', color='g', label="Spec_Min")
    ax1.axhline(y=Spec_Max, linestyle='-.', color='r', label="Spec_Max")
    ax1.axhline(y=Median, linestyle='--', color='b', label="Median")

    ax1.xaxis.set_tick_params(rotation=70, labelsize=10.5)
    ax1.set_xlabel(" ", size=12.5, fontdict=dict(weight='bold'), labelpad=36)
    ax1.set_ylabel(str(units), size=12.5, fontdict=dict(weight='bold'), labelpad=10)
    ax1.set_title(col, size=16, y=1.02, fontdict=dict(weight='bold'))
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.19), fancybox=False, shadow=False, ncol=10,
               edgecolor='black',prop={'size': 12})

    # creating single boxplot for testcase column#
    bp = ax2.boxplot(df[col], vert=0, widths=0.5, patch_artist=True,whis='range')
    for median in bp['medians']:
        median.set(color='k', linewidth=1, )
        x, y = median.get_data()
        xn = (x - (x.sum() / 2.)) * 0.5 + (x.sum() / 2.)
        ax2.plot(xn, y, color="k", linewidth=5, solid_capstyle="butt", zorder=4)
    ax2.axvline(x=Min, linestyle='--', color='k', label=Min)
    ax2.axvline(x=Max, linestyle='--', color='k', label=Max)
    ax2.text(Min,0, Min, va='top', ha="right", bbox=dict(facecolor="w", alpha=0.5),
             transform=ax2.get_xaxis_transform(), size=11.5,rotation=70 )
    ax2.text(Max,0, Max, va='top', ha="right", bbox=dict(facecolor="w", alpha=0.5),
             transform=ax2.get_xaxis_transform(), size=11.5,rotation=70 )
    ax2.axvline(x=Spec_Min, linestyle='-.', color='g', label="Spec_Min")
    ax2.axvline(x=Spec_Max, linestyle='-.', color='r', label="Spec_Max")
    ax2.axvline(x=Median, linestyle='--', color='b', label="Median")
    ax2.xaxis.set_tick_params(rotation=70, labelsize=10, )
    ax2.set_xlabel(str(units), size=12.5, fontdict=dict(weight='bold'), labelpad=10)
    ax2.set_title(col, size=16, y=1.02, fontdict=dict(weight='bold'))
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), fancybox=False, shadow=False, ncol=10,
               edgecolor='black', prop={'size': 12})

    for axis in ['top', 'bottom', 'left', 'right']:
        ax1.spines[axis].set_linewidth(2)
        ax1.spines[axis].set_color("black")
        ax1.spines[axis].set_zorder(0)
        ax2.spines[axis].set_linewidth(2)
        ax2.spines[axis].set_color("black")
        ax2.spines[axis].set_zorder(0)

    plt.show()
    f1_outpath = out_path+"\\" + str(k)+col[0:13].replace(":","_") + ".png"
    f1.savefig(f1_outpath, bbox_inches='tight')
    f2_outpath = out_path + "\\" + str(k) + "s" + col[0:13].replace(":", "_") + ".png"
    f2.savefig(f2_outpath, bbox_inches='tight')
    plt.cla()
print("completed")

