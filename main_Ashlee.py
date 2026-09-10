import pandas as pd

df = pd.read_csv("/Users/ashleehyun/Desktop/Comp BME/Mod 1/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

for header in df.columns:
    print(header)
    