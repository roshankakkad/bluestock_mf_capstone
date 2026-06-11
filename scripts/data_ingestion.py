import pandas as pd
from pathlib import Path

data_path = Path("data/raw")

files = list(data_path.glob("*.csv"))

for file in files:

    df = pd.read_csv(file)

    print("\n" + "="*50)
    print(file.name)
    print("="*50)

    print("Shape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nHead:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())
