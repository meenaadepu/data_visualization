import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import os
from textwrap import wrap
import numpy

outpath = r"C:\Users\testuser\Desktop\Desktop\2228_GTV\18SA"
dir = r'C:\Users\testuser\Desktop\Desktop\2228_GTV\18SA'
sns.set(style="white")
excel_files=[]
#Mode = "1.5"
Mode = "1.8"
#Mode="1.2"
#Mode = "3.3"
#Mode="2.5"
#Mode = "retake
#df_VDDIO_names = [1.35,1.5,1.65]
#df_VDDIO_names = [1.08,1.2,1.32]
#df_VDDIO_names = [1.2,1.8,1.5]
df_VDDIO_names = [1.62,1.8,1.98]
#df_VDDIO_names = [2.97,3.3,3.63]
#df_VDDIO_names = [2.25,2.5,2.75]

#creating output folder path#
out_path = os.path.join(outpath, Mode)
if not os.path.exists(out_path):
    os.makedirs(out_path)
print(out_path)
# #combining all files of folders & subfolder in one file#
# for root, dirs, _ in os.walk(dir):
#         for d in _:
#                 s_dir = os.path.join(root, d)
#                 excel_files.append(s_dir)
# all_data = [pd.read_excel(f) for f in excel_files]
# df = pd.concat(all_data, sort=False,ignore_index=True)
df=pd.read_excel(r"C:\Users\testuser\Desktop\18SA\DC_final_ipu.xlsx")
print(df.shape)

cols = list(df.columns)
cols = [x.replace('<','_').replace('>','') if ('<' or '>') in x else x for x in cols]
df.columns = cols
fcols = cols[6:]
#fcols=["IIL(nA)"]
#fcols=["IIH(nA)","IIL(nA)"]
#fcols=["Hysteresis(V)"]
#fcols=["VOL_DRV<00>","VOL_DRV<01>","VOL_DRV<10>","VOL_DRV<11>"]
#fcols=["VIL(SMT=0)","VIL(SMT=1)",""]
#fcols = ["IPU(uA)","IPD(uA)"]
#process = df['Process'].unique()
#temp = set(df['Temp'])
temp=[-40,25,105,125]
# df_VDDIO_names.sort()
# print(df_VDDIO_names)
#df_VDDC_names = df['VDDC(V)'].unique()
#df_VDDC_names=[0.65,0.8,0.9]
df_VDDC_names=[0.72,0.8,0.88,0.9,0.945]
df_VDDC_names.sort()
df_VDDC_names = ["VDDC " + str(x) for x in df_VDDC_names]
df_VDDIO_names = ["VDDIO " + str(x) for x in df_VDDIO_names]
df["name"] = df["Temp"].astype(str).replace('-','N')+df["VDDC(V)"].astype(str).replace('.','p')+df["VDDIO(V)"].astype(str).replace('.','p')
df["xtick_VDDIO(V)"] ="VDDIO_"+ df["VDDIO(V)"].astype(str)+"V"


for col in fcols:
    print(col)
    fig = plt.figure(figsize=(20, 8))
    ax1 = fig.add_subplot(111)
    #axk=ax1.twinx()
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
    ref=[]
    ref1=[]
    refk=[]
    for i in temp:
        for k, ele in enumerate(df_VDDIO_names):
            s_v = ele[6:]
            count_c = 0
            for j in df_VDDC_names:
                v = j[5:]
                df_filter = df[(df['Temp'] == float(i)) & (df['VDDIO(V)'] == float(s_v)) & (df['VDDC(V)'] == float(v))]
                if not df_filter.empty:
                   # color_dict = dict({'FF': '#2980B9', 'FS': 'green', 'SF': 'violet', 'SS': 'orange', 'TT': 'coral',
                   #                         'Min Design Spec': "red", 'Max Design Spec': "red"})
                   # markers = {'FF': 'o', 'FS': 'o', 'SF': 'o', 'SS': 'o', 'TT': 'o', 'Min Design Spec': "X",
                   #                  'Max Design Spec': "X"}
                   color_dict = dict({'FF': '#2980B9', 'FS': 'green', 'SF': 'violet', 'TT': 'tan', 'SS': 'coral','Design Spec':'red'})
                   markers = {'FF': 'o', 'FS': 'o', 'SF': 'o', 'SS': 'o', 'TT': 'o','Design Spec': "X"}
                   # #

                   g=sns.scatterplot(x='name', y=col, hue='Process',s=100,edgecolor = 'black',style="Process",markers=markers,palette=color_dict,data=df_filter,legend='full')
                   df1 = df_filter[df_filter["Process"]=="Design Spec"]
                   ref.extend(list(df1[col]))
                   # ax1.plot(ref, color='red', linewidth=3)
                   # df2 = df_filter[df_filter["Process"]=="Min Design Spec"]
                   # ref1.extend(list(df2[col]))
                   # ax1.plot(ref1, color='red', linewidth=3)
                   # df1 = df_filter[df_filter["Process"]=="Design Spec"]
                   # ref.extend(list(df1[col]))
                   # ax1.plot(ref, color='red', linewidth=3)
                   #g.plot(, df_filter, 'b-', linewidth = 2)
                   #plt.plot([0, 4], [1.5, 0], linewidth=2)
                   #for k1 in g.axes.flat:
                   # k1.plot(x='name', y=col, hue='Process',style="Process",markers=markers,palette=color_dict,data=df_filter,legend='full')
                   #g.plot(x_func, y=col,label='Design Spec')
                   l.append(v)
                   count_c = count_c + 1
            vd = vd + count_c
            l2.append(vd-1)
            test_list = [None] * (vd)
            pos = vd - count_c
            test_list[pos:pos] = ref
            print(ref,count_c,vd,test_list)
            if (col == 'IIH(nA)' or col == 'IPU(uA)'  or col =='IIL(nA)' or col =='IPD(uA)'):
                ax1.plot(ref, color='red', linewidth=3, )
            else:
                ax1.plot(test_list, color='red', linewidth=3, )
                ref=[]
        l2_vio.extend(df_VDDIO_names)
        l3.append(vd)
    l3_t.extend(temp)
    # fig, ax1 = plt.subplots(figsize=(4,4))
    # ax2 = ax1.twinx()
    # sns.barplot(x=['A','B','C','D'],
    #             y=[100,200,135,98],
    #             color='#004488',
    #             ax=ax1)
    # sns.lineplot(x=['A','B','C','D'],
    #              y=[4,2,5,3],
    #              color='r',
    #              marker="o",
    #              ax=ax2)
   # yvalues = plt.get_ydata()
    #print(yvalues)
    # setting VDDC tick labels on plot#
    labels_io = ['\n'.join(wrap("VDDC   "+k+"V", 6)) for k in l]
    g.set_xticklabels(labels_io,fontweight='bold',color='black',fontsize='10')
    #ax1.tick_params(labelsize=10)
    #plt.rcParams["ax1.labelweight"] = "bold"
    y_value=['{:,.2f}'.format(x) for x in ax1.get_yticks()]
    print(y_value)
    g.set_yticklabels(y_value,fontsize=12,fontweight='bold',color='black')
    #plt.rcParams['ytick.fontweight']='bold'
    #g.set_xticklabels.set_color("red")
    #ax1.label1.set_fontsize(14)
    #ax1.label1.set_fontweight('bold')
    if (col == 'IIL(nA)' or col == 'IIH(nA)'):
         ax1.set_yscale("log")
         ax1.set_ylim((10**-2,10**5))
    # setting legend labels on plot#
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    new_legends_keys = list(by_label.keys())[1:]
    # g.legend(list(by_label.values())[1:], list(by_label.keys())[1:], loc='upper center', bbox_to_anchor=(0.5, -0.2),
    #           fancybox=False, shadow=False, ncol=6, edgecolor='black')
    # if( col == 'IPD(uA)' or col == 'IPU(uA)'):
    #     if(wd=="Design Spec" for wd in new_legends_keys):
    if ( col == 'IPD(uA)' or col == 'IPU(uA)' or col == 'VOH(DRV=00)' or col == 'VOH(DRV=01)' or col =='VOH(DRV=10)' or  col == 'VOH(DRV=11)' or col == 'VIL(SMT=0)' or col =='VIL(SMT=1)' or col == 'Hysteresis(V)'):
        replaced = ['Min Design Spec' if wd == "Design Spec" else wd for wd in new_legends_keys]
        xmin, xmax = ax1.get_xbound()
        print(xmin,xmax)
        g.legend(list(by_label.values())[1:], replaced, loc='upper center', bbox_to_anchor=(0.5, -0.2),
                 fancybox=False, shadow=False, ncol=6, edgecolor='black')

    elif(col == 'Hysteresis(V)'):
        replaced = ['Min Design Spec' if wd == "Design Spec" else wd for wd in new_legends_keys]
        g.legend(list(by_label.values())[1:], replaced, loc='upper center', bbox_to_anchor=(0.5, -0.2),
                 fancybox=False, shadow=False, ncol=6, edgecolor='black')
    else:
        replaced = ["Max Design Spec" if wd == "Design Spec" else wd  for wd in new_legends_keys]
        xmin, xmax = ax1.get_xbound()
        print(xmin,xmax)
        g.legend(list(by_label.values())[1:], replaced, loc='upper center', bbox_to_anchor=(0.5, -0.2),
                 fancybox=False, shadow=False, ncol=6, edgecolor='black')
    plt.setp(g.get_legend().get_texts(), fontsize='12',fontweight='bold')


    ax2 = g.twiny()
    ax3 = g.twiny()
    ax4 = g.twiny()
    ax5 = g.twiny()

    #setting VDDIO tick labels on plot#
    n_l2_vio =[]
    n_l2=list(set(l2))
    print(l2)
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
    print(l2_vio)
    labels = ['\n'.join(wrap(l+"V", 5)) for l in n_l2_vio]
    ax2.set_xticklabels(labels, fontsize=30,fontweight='bold',color='black')
    ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
    ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
    ax2.tick_params(which='major', length=35, width=0, direction='out',labelsize = 10)
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
    labels_temp=(str(i)+str("C") for i in l3_t)
    #ax3.set_xticklabels(str(i)+str("C") for i in l3_t)
    ax3.set_xticklabels(labels_temp,fontsize=7,fontweight='bold',color='black')
    #ax3.set_xticklabels(l3_tn, fontsize=7,fontweight='bold',color='black')
    ax3.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
    ax3.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
    ax3.tick_params(which='major', length=70, width=0, direction='out',labelsize = 14)
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
    Title = col +' Measured across PVT in ' + Mode +'V Mode'
    #Title = col +' Measured across VT'
    ax1.set_title(Title, size=16, y =1.02,fontdict=dict(weight='bold'))
    ax1.set_xlabel(" ", size=14, fontdict=dict(weight='bold'),labelpad=40)
    if (col == 'IPD(uA)' or col == 'IPU(uA)'):
        ax1.set_ylabel(col, size=14, fontdict=dict(weight='bold'), labelpad=10,fontweight='bold')
        plt.rcParams['ytick.labelsize']=10
    elif (col == 'IIL(nA)' or col == 'IIH(nA)'):
         ax1.set_ylabel(col[0:3]+"(Log)", size=14, fontdict=dict(weight='bold'), fontweight='bold',color='black',labelpad=10)
         plt.rcParams['ytick.labelsize']=10
    else:
        ax1.set_ylabel(col[0:3]+"(V)", size=14, fontdict=dict(weight='bold'), fontweight='bold',color='black',labelpad=10)
        plt.rcParams['ytick.labelsize']=10

    for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(2.5)
        ax1.spines[axis].set_color("black")
        ax1.spines[axis].set_zorder(0)
   # plt.show()
    fig_outpath = out_path +'\\' + col + Mode + ".png"
    fig.savefig(fig_outpath, bbox_inches='tight')
    plt.cla()

print("Completed")



