import pandas as pd
from tkinter import filedialog

def file_to_df(filepath):
    file_df = pd.read_csv(filepath)
    return file_df

def write_to_file(df, tree):
    # file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    # if not file_path:
    #     print("Cancelled")
    # else:
    #     df.to_csv(file_path, index=False)
    return 0