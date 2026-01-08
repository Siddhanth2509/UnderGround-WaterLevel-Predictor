import pandas as pd

df = pd.read_csv("Data/DWLR_Dataset_2023.csv")
print(df["Water_Level_m"].describe())
