from matplotlib import pyplot as plt
from pyecharts.charts import Page
import seaborn as sns
import creat#这是有绘制各种图形函数的类
import generated_data#这是来生成数据的类
import itemsyle_all#这是有各种图形格式的类
import pandas as pd
#在此处生成所有的需要展示的图像!!!
data = pd.read_csv('./data/二手车上牌数据处理.csv')
data2 = pd.read_csv('./data/修改后按年分的文件.csv')
# 将字符串日期转换为日期类型
data['上牌时间'] = pd.to_datetime(data['上牌时间'])
data['年检到期'] = pd.to_datetime(data['年检到期'])
data['保险到期'] = pd.to_datetime(data['保险到期'])
data_list = ['车辆级别', '车身颜色','驱动方式','label_price','label1_行驶距离']
# 设置字体为微软雅黑，确保中文显示正常
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置正常显示负号
plt.rcParams['axes.unicode_minus'] = False
#得到按顺序排列的年份
year = data['year'].unique().tolist()
year = sorted(year)
# 绘制出tab展示基本变量的时间条形图
creat.draw_tab(data,data_list,year,itemsyle_all.itemstyle_line).render('result/tab展示各年变量的变化.html')
# 绘制品牌数量前top饼图
creat.draw_pie(data,itemsyle_all.pie_style,'brands',10,'车辆品牌前十的数量').render('./result/车辆品牌的前十饼图.html')
# # 绘制驱动方式前十数量的柱形图
creat.draw_single_bar(data,itemsyle_all.bar_style,'车辆级别',10,'驱动方式').render('./result/驱动方式的前十柱形图.html')
#在售车辆的颜色统计
creat.draw_pie(data,itemsyle_all.pie_style,'车身颜色',8,'车身颜色数量的统计').render('./result/车身颜色数量的统计.html')
#在售车辆的驱动方式数量统计
creat.draw_single_bar(data,itemsyle_all.bar_style,'驱动方式',6,'车辆驱动方式的数量统计').render('./result/车辆驱动方式的数量统计.html')
# #绘制不同车辆颜色喜爱程度柱形图.html
dp = generated_data.get_single_by_single(data,'brands','车身颜色',10)
creat.draw_bar(dp,itemsyle_all.bar_style,'不同车辆颜色喜爱程度柱形图','brands','车身颜色').render('./result/不通车辆颜色喜爱程度柱形图.html')
# plot绘制
#x='行驶距离(万公里)',y='price',hue='车辆级别'
creat.plot_vehicle_data(data).savefig('./result/x=行驶距离(万公里),y=price,hue=车辆级别.png')
# # x=year,y=行驶距离(万公里),hue=车辆级别
creat.plot_vehicle_data(data, x='year',y='行驶距离(万公里)',hue='车辆级别').savefig('./result/x=year,y=行驶距离(万公里),hue=车辆级别.png')
creat.plot_vehicle_data(data, x='驱动方式', y='price',hue='车辆级别').savefig('./result/x=x=驱动方式, y=price,hue=车辆级别.png')
# 绘制主要考虑因素近几年静态分析图
page1 = Page(layout=Page.SimplePageLayout)
page1.add(
creat.draw_pie(data,itemsyle_all.pie_style,'brands',10,'车辆品牌前10的分布'),
    creat.draw_single_bar(data,itemsyle_all.bar_style,'车辆级别',10,'驱动方式'),

)
page1.render("./result/combined_charts1.html")
page2 = Page(layout=Page.SimplePageLayout)
page2.add(

creat.draw_pie(data,itemsyle_all.pie_style,'车身颜色',8,'车身颜色的数量统计'),
creat.draw_single_bar(data,itemsyle_all.bar_style,'驱动方式',6,'车辆驱动方式的数量统计')
)
page2.render("./result/combined_charts2.html")
dp1 = data.groupby(['year','brands'])['price'].mean().reset_index()
dp1.columns = ['year','brands','price']
dp1['price'] = dp1['price'].apply(lambda x:int(x))
dp1 = dp1.values.tolist()
creat.draw_price_average(year,dp1,itemsyle_all.itemstyle_line).render('./result/每一年各品牌的平均价格.html')
data_pair_color = data.groupby('brands')['车身颜色'].count().sort_values(ascending=False).reset_index().values.tolist()[:10]
page3 = Page()
page3.add(
    creat.draw_bar(data_pair_color,itemsyle_all.bar_style,'不同车辆颜色喜爱程度柱形图','brands','车身颜色'),
    creat.draw_bar1(data,itemsyle_all.itemstyle_bar,itemsyle_all.itemstyle1_bar1)
)
page3.render('./result/page1.html')
page4 = Page()
page4.add(
    creat.bar_over_line(data2),
    creat.draw_line2(data2)
)
page4.render('./result/page2.html')
#绘制价格区间车辆的饼图
creat.draw_pie(data,itemsyle_all.pie_style,'label_price',10,'各价格区间的车辆').render('./result/各价格区间的车辆.html')
creat.get_data6(data,year).render('./result/上牌时间间隔.html')
# #绘制可视化分析图集
creat.draw_album(data).savefig('result/图集.png')
# #得到涉及车险的饼图
creat.get_insurance_pie(data,data_score='年检到期').render('./result/年检到期的饼图分布.html')
creat.get_insurance_pie(data,data_score='保险到期').render('./result/保险到期的饼图分布.html')
creat.get_insurance_pie(data,data_score='上牌时间').render('./result/上牌时间的饼图分布.html')

creat.plot_trend_analysis(data).savefig('result/上课时间、年检到期和保险到期分布.png')

creat.analyze_intervals(data).savefig('result/保险、年检与上牌时间的间隔.png')

creat.analyze_vehicle_expiration(data).savefig('result/上牌时间与年检、保险到期的关系.png')

creat.draw_scatter(data2).render('result/行驶距离与年份的变化.html')

creat.draw_word_cloud(data).render('result/所有品牌的词云图.html')
