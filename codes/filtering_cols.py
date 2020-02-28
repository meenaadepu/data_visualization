import pandas as pd
import os

f = r'D:\Meena\Automation\ABB\ABB_extracted_data_BBGENN.csv'
df = pd.read_csv(f)
filter_col="_0.65_.*"
df= df.filter(regex=filter_col, axis=1)
#df = pd.concat(all_data, sort=False,ignore_index=True)
df.to_csv(r"D:\Meena\Automation\ABB\ABB_extracted_data_BBGENN_0.65.csv")
print(df.shape)


