import pandas as pd

df = pd.read_csv("/Users/ikedo/OneDrive/Desktop/Computational BME/Module 1/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

for column in df.columns:
    print(column)
