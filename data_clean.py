# 完成数据清洗的模块
import numpy as np
import pandas as pd
df=pd.read_csv('./data/二手车已上牌.csv')
# 提取品牌的函数
def extract_brand(car_str):
    parts = car_str.split()
    if len(parts) > 0:
        first_part = parts[0]

        # 检查是否全是中文
        if any('\u4e00' <= char <= '\u9fff' for char in first_part):
            # 如果全是中文或者中文后接非中文字符，则取中文部分
            for i, char in enumerate(first_part):
                if not ('\u4e00' <= char <= '\u9fff'):
                    return first_part[:i]  # 返回中文部分作为品牌
            return first_part  # 如果全是中文
        # 检查是否全是数字
        elif first_part.isdigit():
            return first_part  # 如果是数字，则返回数字字符串
        # 检查是否是英文字母

        elif first_part[0].isupper() and first_part[0].isalpha():
            return first_part
    return ''  # 如果不符合条件，则返回空字符串


# 应用函数提取品牌
df['brands'] = df['title'].apply(extract_brand)

# 替换特定的品牌
df['brands'] = df['brands'].replace('一汽', '一汽-大众')
df['brands'] = df['brands'].replace('北京', '北京BJ40')
df.loc[df.index[[33, 91, 407, 632]], 'brands'] = 'RAV4荣放'
df.loc[df.index[158], 'brands'] = 'T-ROC探歌'
df.loc[df.index[298], 'brands'] = 'QQ冰淇淋'
df.loc[df.index[96], 'brands'] = '发现'
df.loc[df.index[221], 'brands'] = '发现'
mask = df['brands'].str.contains('揽胜')
df.loc[mask, 'brands'] = '揽胜'
bins = [2.3, 4.27, 6.23, 8.2, 10.17, 12.13, 14.1, 16.07, 18.03, 20.0, 100]
df['label_price'] = pd.cut(df['price'], bins=bins, right=True,
                           labels=['2.30 - 4.27', '4.27 - 6.23', '6.23 - 8.20', '8.20 - 10.17', '10.17 - 12.13',
                                   '12.13 - 14.10',
                                   '14.10 - 16.07', '16.07 - 18.03', '18.03 - 20.00', '大于20'])
bins1 = [0.00, 3.01, 6.01, 9.01, 12.01, 1000]
labels1 = ['0.00-3.01', '3.01-6.01', '6.01-9.01', '9.01-12.01', '大于12.01']

df['label1_行驶距离'] = pd.cut(df['行驶距离(万公里)'], bins=bins1, labels=labels1)
df.to_csv('./data/二手车上牌数据处理.csv')