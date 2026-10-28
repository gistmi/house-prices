import pandas as pd

train = pd.read_csv("data/raw/train.csv")

print(train.shape)
print(train["Saleprice"].describe())