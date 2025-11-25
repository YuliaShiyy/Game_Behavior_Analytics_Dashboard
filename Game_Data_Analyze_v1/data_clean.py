# @Author : Yulia
# @File   : data_clean.py
# @Time   : 2025/8/26 0:02
import pandas as pd

# 1. 加载数据
df = pd.read_csv("./OnlineGamingBehavior/online_gaming_behavior_dataset.csv")

# 2. 快速查看数据结构
print(df.shape)        # 行数和列数
print(df.info())       # 每列数据类型、缺失情况
print(df.head())       # 前5行

# 3. 基础清洗
# 去掉重复值
df = df.drop_duplicates()

# 4. 简单EDA
print(df['Location'].value_counts())
print(df['GameGenre'].value_counts())
print(df.describe())

# 5. 选取欧洲玩家子集
df_europe = df[df['Location'] == 'Europe']

# 保存清洗后的数据
df.to_csv("gaming_data_cleaned.csv", index=False)
df_europe.to_csv("gaming_data_europe.csv", index=False)

print("数据清洗完成 ✅")
