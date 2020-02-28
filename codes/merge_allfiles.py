import pandas as pd
import os

dir = r'E:\Meena\Automation\plots\inputs\2228\GPIO18_AE\18_AE_PVT_DATA'
excel_files=[]

#extracting all filenames in folder with subfoldersfiles#
for root, dirs, _ in os.walk(dir):
        for d in _:
                s_dir = os.path.join(root, d)
                excel_files.append(s_dir)

print(excel_files)
#excel_files=[ x for x in excel_files if "FF" not in x ]
print(excel_files)
all_data = [pd.read_excel(f) for f in excel_files]
df = pd.concat(all_data, sort=False,ignore_index=True)
df.to_excel(r"E:\Meena\Automation\plots\outputs\18_ae_pvt.xlsx")
print(df.shape)


