import pandas as pd
import json
import os
import pathlib
from openpyxl import load_workbook

df = pd.read_excel(r"D:\Meena\Automation\correlation\siliconfull.xlsx",sheet_name='ROS7p5T')
df_sim = pd.read_excel(r"D:\Meena\Automation\correlation\7p5tSIMfull.xlsx")
path_grph =r"D:\Meena\Automation\correlation"
path1 =r"D:\Meena\Automation\correlation\output.xlsx"
path2 =r"D:\Meena\Automation\correlation\output_grphs.xlsx"
writer1 = pd.ExcelWriter(path1, engine='xlsxwriter')

with open(r'D:\Meena\Automation\plots\codes\2_filter_mean_config.json') as f:
    config = json.load(f)

process = df['Process'].unique()
temp = df['Temp'].unique()
vref = df['Vref'].unique()
vddc = df['VDDC(V)'].unique()
code = df['Code'].unique()
cells = list(df.columns)
cells=[x for x in cells if 'VT' in x]


def get_sim_values(l1):
    cl = l1[5][-2:]+l1[5][0]
    print(l1,cl)
    df_sim_filter = df_sim[(df_sim['Process'] == l1[0]) & (df_sim['Temperature (C)'] == l1[1]) & (df_sim['VREF'] == l1[3])  & (df_sim['Voltage (V)'] == l1[2])& (df_sim['Code'] == l1[4])& (df_sim['Cell_name'] == cl)]
    sim_value = df_sim_filter['Frequency(Hz)'].values
    return  sim_value

for cel in cells:
    sht_name = cel
    l2 = []
    for p in process:
        for t in temp:
            for vr in vref:
                for vd in vddc:
                    for c in code:
                        l1 = []
                        l = []
                        df_filter = pd.DataFrame()
                        df_filter = df[(df['Process'] == str(p)) & (df['Temp'] == float(t))  & (df['Vref'] ==float(vr)) & (df['VDDC(V)'] == float(vd))& (df['Code'] == int(c))]
                        m = df_filter[cel].mean()
                        m = m*1000000
                        l.append(p)
                        l.append(t)
                        l.append(vd)
                        l.append(vr)
                        l.append(c)
                        l.append(cel)
                        l.append(m)
                        l1.extend(l)
                        s_value = get_sim_values(l1)
                        if len(s_value) == 0:
                            s_value=[-1]
                        if len(s_value) > 0:
                            s_value = [s_value[0]]
                        l1.extend(s_value)
                        d = ((s_value[0] - (m)) / s_value[0])
                        l1.extend([d])
                        l2.append(l1)

    df1 = pd.DataFrame(l2,columns=['Process', 'Temp', 'VDDC(V)','Vref(V)','Code', 'CellName','mean','sim','Delta'])
    df1.to_excel(writer1, sheet_name=sht_name, index=False)
    df1 = df1[(df1['sim'] != -1)]
    df_out=df1

    for volt_drive in config['rosc_delay'].keys():
        out_dir = os.path.join(path_grph, volt_drive)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        df_out_f = pd.DataFrame()
        for i, data in enumerate(config['rosc_delay'][volt_drive]):
            print(volt_drive)
            out_fname = cel +".xlsx"
            path_f = os.path.join(out_dir, out_fname)
            writer2 = pd.ExcelWriter(path_f, engine='xlsxwriter')
            col_name = '%s_%s_%s_%s' % (data['process'], data['temp'],data['vref'],data['vddc'])
            df_out1 = pd.DataFrame()
            df_out_filter = df_out[(df_out['Process'] == data['process']) & (df_out['Temp'] == data['temp']) &(df_out['Vref(V)'] == data['vref']) & (df_out['VDDC(V)'] == data['vddc'])]
            df_out1 = pd.DataFrame(list(zip(df_out_filter['Code'],(df_out_filter['Delta']))), columns=['Code',col_name])
            df_out_f = pd.concat([df_out_f, df_out1],axis=1, sort=False)
            df_out_f = df_out_f.T.drop_duplicates().T

        df_out_f = df_out_f.loc[:, ~df_out_f.columns.duplicated()]
        df_out_f.to_excel(writer2, sheet_name=cel, index=False)
        print(df_out_f.head(3))
        workbook = writer2.book
        worksheet = writer2.sheets[sht_name]
        mark_color = {'TT_25': ['diamond', 'red'], 'TT_85': ['diamond', '#A62D2D'],
                      'TT_125': ['diamond', '#1ee5bc'], 'TT_-40': ['diamond', '#f5228f'],
                      'SS_-40': ['triangle', '#f53b22'],
                      'SS_125': ['triangle', '#331212'],
                      'FS_-40': ['circle', '#ffc000'], 'FS_125': ['circle', '#4472c4'],
                      'SF_-40': ['circle', '#ffc000'], 'SF_125': ['circle', '#4472c4'],
                      'FF_-40': ['circle', '#ffc000'], 'FF_125': ['circle', '#4472c4']}
        percent_fmt = workbook.add_format({'num_format': '0.00%'})
        worksheet.set_column('B:F', None, percent_fmt)
        chart = workbook.add_chart({'type': 'line', 'color': 'red'})
        for i in range(len(list(df_out_f)) - 1):
            row = df_out_f.shape[0]
            col = i+1
            s = list(df_out_f)[col]
            print(s)
            #print(list(df_out_f))
            m_c_key = str(s.split('_')[0] + '_' + s.split('_')[1])
            marker, color = mark_color.get(m_c_key)
            print(m_c_key,marker, color)
            chart.add_series({
                'name': [sht_name, 0, col],
                'categories': [sht_name, 1, 0, row, 0],
                'values': [sht_name, 1, col, row, col],
                'marker': {'type': marker, 'size': 7, 'line': {'color': color}, 'border': {'color': color},
                           'fill': {'color': color}},
                'line': {'none': True}
            })
        chart.set_size({'width': 1000.00, 'height': 550.00, })
        chart.set_plotarea({'layout': {'x': 0.09, 'y': 0.22, 'width': 0.90, 'height': 0.50, }})
        title = "%s %s ROSC" % ("7P5T", cel)
        chart.set_title({'name': title,'name_font': {'name': 'Arial', 'color': 'black', 'size': 14, 'bold': True},'overlay': True,})

        # Configure the chart axes.
        chart.set_x_axis({'num_font': {'rotation': -45, 'name': 'Arial', 'size': 8, 'bold': True},
                                  'major_gridlines': {'visible': True},
                                  'label_position': 'low',
                                  'name': cel,
                                  'name_font': {'name': 'Arial', 'size': 10, 'bold': True},
                                  })

        chart.set_y_axis({'major_gridlines': {'visible': False},
                                  'num_font': {'name': 'Arial', 'size': 10, 'bold': True},
                                  'name': 'Simulation vs Silicon Error in %',
                                  'name_font': {'name': 'Arial', 'size': 10, 'bold': True},
                                  })

        chart.set_legend({'layout': {'x': 0.03, 'y': 0.10, 'width': 0.95, 'height': 0.10, },
                          'font': {'name': 'Arial', 'size': 10}})
        worksheet.insert_chart('I2', chart)
        print(cel,"kkk")
        writer2.save()




writer1.save()
writer1.close()
writer2.close()


