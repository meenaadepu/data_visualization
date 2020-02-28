import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
out_path = "D:\Meena\Automation\plots\DPHY\outputs"
sns.set_style("whitegrid")
df = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet1")
df_ref = pd.read_excel("D:\Meena\Automation\plots\DPHY\inputs\DPHY_Tx_Protocol_tests_Final.xlsx",sheet_name="Sheet2")
cols = list(df.columns)
df.columns = cols
fcols = cols[6:]

df["name"] = df["Temp"].astype(str)+df["Voltage"].astype(str)+df["Corner"].astype(str)
color_dict = dict({'FF': '#2980B9', 'FS': 'green', 'SF': 'violet', 'SS': 'orange', 'TT': 'crimson'})
medianprops = dict(linestyle='--', linewidth=5, color='k')

for k ,col in enumerate(fcols):
    print(col)
    f1 = plt.figure(figsize=(18, 7))
    ax1 = f1.add_subplot(111)
    Spec_Min = float((df_ref[col][0:1]))
    Spec_Max = float((df_ref[col][1:2]))
    units =   df_ref[col][2:3].values
    Median = df[col].median()
    print(Spec_Min, Spec_Max,Median,units)

    sns.boxplot(data=df, x='name', y=col, hue='Corner',palette=color_dict,ax=ax1,medianprops=medianprops)

    ax1.axhline(y=Spec_Min, linestyle='-.', color='g',label ="Spec_Min")
    ax1.axhline(y=Spec_Max, linestyle='-.',color='r',label ="Spec_Max")
    ax1.axhline(y=Median, linestyle='--',color='b',label ="Median")

    ax1.xaxis.set_tick_params(rotation=70,labelsize = 10)
    ax1.set_xlabel("PVT", size=12.5, fontdict=dict(weight='bold'), labelpad=36)
    ax1.set_ylabel(str(units), size=12.5, fontdict=dict(weight='bold'), labelpad=10)
    ax1.set_title(col, size=16, y=1.02, fontdict=dict(weight='bold'))
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), fancybox=False, shadow=False, ncol=10,edgecolor='black',
               prop={'size': 12})

    for axis in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[axis].set_linewidth(2)
        plt.gca().spines[axis].set_color("black")
   # plt.show()
    f1_outpath = out_path+"\\" + str(k)+col[0:10].replace(":","_") + ".png"
    f1.savefig(f1_outpath, bbox_inches='tight')
    plt.cla()
print("completed")

