import pandas as pd
from interactive_trader.synchronous_functions import enter_trade

csv_file = "worriors_data_raw.csv"
csv_data = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
csv_df = pd.DataFrame(csv_data)
del csv_df['Unnamed: 9'], csv_df['Unnamed: 10'], csv_df['Unnamed: 11'], csv_df['Unnamed: 12']
result = enter_trade(60, csv_df, 1)

print(result)