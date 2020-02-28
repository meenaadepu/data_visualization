import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import os
from textwrap import wrap

outpath = r"D:\Meena\Automation\plots\outputs\18_AE_PVT_DATA"
dir = r'D:\Meena\Automation\plots\inputs\2228\GPIO18_AE\18_AE_PVT_DATA'
sns.set(style="white")
excel_files=[]
Mode = "1.5"
df_VDDIO_names = [1.5,1.35,1.65]

#creating output folder path#
out_path = os.path.join(outpath, Mode)
if not os.path.exists(out_path):
    os.makedirs(out_path)

#combining all files of folders & subfolder in one file#
for root, dirs, _ in os.walk(dir):
        for d in _:
                s_dir = os.path.join(root, d)
                excel_files.append(s_dir)
all_data = [pd.read_excel(f) for f in excel_files]
df = pd.concat(all_data, sort=False,ignore_index=True)
df.to_excel(r"D:\Meena\Automation\plots\outputs\18_ae_pvt.xlsx")
print(df.shape)

cols = list(df.columns)
cols = [x.replace('<','_').replace('>','') if ('<' or '>') in x else x for x in cols]
df.columns = cols
fcols = cols[6:]

process = df['Process'].unique()
temp = set(df['Temp'])
temp = []
#df_VDDIO_names.sort()
df_VDDC_names = df['VDDC(V)'].unique()
df_VDDC_names.sort()


df_VDDC_names = ["VDDC " + str(x) for x in df_VDDC_names]
df_VDDIO_names = ["VDDIO " + str(x) for x in df_VDDIO_names]
df["name"] = df["Temp"].astype(str).replace('-','N')+df["VDDC(V)"].astype(str).replace('.','p')+df["VDDIO(V)"].astype(str).replace('.','p')
df["xtick_VDDIO(V)"] ="VDDIO_"+ df["VDDIO(V)"].astype(str)+"V"
print(df_VDDC_names)

for col in fcols:
    print(col)
    fig = plt.figure(figsize=(25, 9))
    ax1 = fig.add_subplot(111)
    l = []
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l2_vio = []
    l3_t = []
    l4_sep = []
    vd = 0
    vt = 0
    for i in temp:
        for k, ele in enumerate(df_VDDIO_names):
            s_v = ele[6:]
            count_c = 0
            for j in df_VDDC_names:
                v = j[5:]
                df_filter = df[(df['Temp'] == float(i)) & (df['VDDIO(V)'] == float(s_v)) & (df['VDDC(V)'] == float(v))]
                if not df_filter.empty:
                   color_dict = dict({'FF': '#2980B9', 'FS': 'green', 'SF': 'violet', 'SS': 'orange', 'TT': 'coral','Design Spec':'red'})
                   markers = {'FF': 'o', 'FS': 'o', 'SF': 'o', 'SS': 'o', 'TT': 'o','Design Spec': "X"}
                   g = sns.scatterplot(x='name', y=col, hue='Process',s=65,edgecolor = 'black',style="Process",markers=markers,palette=color_dict,data=df_filter,legend='full')
                   l.append(v)
                   count_c = count_c + 1
            vd = vd + count_c
            l2.append(vd-1)
        l2_vio.extend(df_VDDIO_names)
        l3.append(vd)
    l3_t.extend(temp)

    # setting VDDC tick labels on plot#
    labels_io = ['\n'.join(wrap("VDDC   "+k+"V", 6)) for k in l]
    g.set_xticklabels(labels_io, fontsize=9)

    if (col == 'IIL(nA)' or col == 'IIH(nA)'):
         ax1.set_yscale("log")
         ax1.set_ylim((10**-3,10**4))

    # setting legend labels on plot#
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    new_legends_keys = list(by_label.keys())[1:]
    if ( col == 'IPD(uA)' or col == 'IPU(uA)' or col == 'VOH_DRV_01' or col == 'VOH_DRV_10' or col =='VOH_DRV_11' or  col == 'VIL_SMT_1' or col == 'VIL_SMT_0'):
        replaced = ['Min Design Spec' if wd == "Design Spec" else wd for wd in new_legends_keys]
        g.legend(list(by_label.values())[1:], replaced, loc='upper center', bbox_to_anchor=(0.5, -0.2),
                 fancybox=False, shadow=False, ncol=6, edgecolor='black')
    else:
        replaced = ["Max Design Spec" if wd == "Design Spec" else wd  for wd in new_legends_keys]
        g.legend(list(by_label.values())[1:], replaced, loc='upper center', bbox_to_anchor=(0.5, -0.2),
                 fancybox=False, shadow=False, ncol=6, edgecolor='black')



    ax2 = g.twiny()
    ax3 = g.twiny()
    ax4 = g.twiny()
    ax5 = g.twiny()

    #setting VDDIO tick labels on plot#

    n_l2_vio =[]
    n_l2=list(set(l2))
    ax2.set_xticks(l2)
    for c in n_l2:
        a = l2.index(c)
        n_l2_vio.append(l2_vio[a])
    v2 = -1
    l2_vion = []
    for y in n_l2:
        med = (v2 + y) / 2
        v2 = y
        l2_vion.append(med+0.5)

    labels = ['\n'.join(wrap(l+"V", 5)) for l in n_l2_vio]
    ax2.set_xticklabels(labels, fontsize=7)
    ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
    ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
    ax2.tick_params(which='major', length=30, width=0, direction='out',labelsize = 9.5)
    ax2.set_xticks(l2_vion)
    ax2.set_xlim(ax1.get_xlim())

   #setting temp ticks position and labels#
    v1  = -1
    l3_tn=[]
    for x in l3:
        m = (v1 + x) / 2
        v1 = x
        l3_tn.append(m-0.5)
   # print(l3_tn)
    ax3.set_xticks(l3_tn)
    ax3.set_xticklabels(str(i)+str("C") for i in l3_t)
    ax3.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
    ax3.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
    ax3.tick_params(which='major', length=65, width=0, direction='out',labelsize = 15)
    ax3.set_xlim(ax1.get_xlim())

   # setting temp separaters ticks position#
    l4_sep= [i-0.5 for i in l3]
    l4_sep.append(-0.5)
    ax4.set_xticks(l4_sep)
    empty_string_labels = ['']
    ax4.set_xticklabels(empty_string_labels)
    ax4.xaxis.set_ticks_position('bottom')
    ax4.tick_params(which='major', length=85, width=2, direction='out')
    ax4.set_xlim(ax1.get_xlim())

    # setting VDDIO separaters ticks position#
    l5_sep= [i+0.5 for i in n_l2]
    ax5.set_xticks(l5_sep)
    empty_string_labels = ['']
    ax5.set_xticklabels(empty_string_labels)
    ax5.xaxis.set_ticks_position('bottom')
    ax5.tick_params(which='major', length=45, width=0.8, direction='out')
    ax5.set_xlim(ax1.get_xlim())

    # setting Title and x,y labels#
    Title = col +' Measuread across PVT in ' + Mode +'V Mode'
    ax1.set_title(Title, size=16, y =1.02,fontdict=dict(weight='bold'))

    ax1.set_xlabel(" ", size=12.5, fontdict=dict(weight='bold'),labelpad=40)
    if (col == 'IIL(nA)' or col == 'IIH(nA)'or col == 'IPD(uA)' or col == 'IPU(uA)'):
        ax1.set_ylabel("µA", size=12.5, fontdict=dict(weight='bold'), labelpad=10)
    else:
        ax1.set_ylabel("V", size=12.5, fontdict=dict(weight='bold'), labelpad=10)

    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(2.5)
        ax1.spines[axis].set_color("black")
        ax1.spines[axis].set_zorder(0)
   # plt.show()
    fig_outpath = out_path +'\\' + col + Mode + ".png"
    fig.savefig(fig_outpath, bbox_inches='tight')
    plt.cla()

print("Completed")



