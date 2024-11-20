import pandas as pd
from matplotlib import pyplot as plt
from pyecharts.charts import Pie, Timeline, Line, Bar, Tab, WordCloud

import pyecharts.options as opts
from pyecharts.globals import ThemeType
import seaborn as sns
import generated_data
import itemsyle_all
from pyecharts.charts import Scatter

#绘制某一个属性前多少的饼图
def draw_pie(data,itemstyle_pie,data_score,top,title,radius=['30%', '80%'],rosetype='area',):
    data_pair  = generated_data.get_one_top(data,data_score,top)
    pie = (Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
           .add(series_name=title, data_pair=data_pair,
                radius=radius,  # 饼图内半径和外半径
                rosetype=rosetype,  # 否展示成南丁格尔图
                label_opts=opts.LabelOpts(formatter='{b}:{c}\n百分占比{d}%'),  # 标签配置
                itemstyle_opts=itemstyle_pie,  # 图元样式配置
                emphasis_opts=opts.EmphasisOpts(is_show_label_line=True, focus='series',
                                                label_opts=opts.LabelOpts(font_size=20, font_weight='bold')
                                                ),  # 高亮多边形配置
                )
           #     .set_colors()
           .set_global_opts(tooltip_opts=opts.TooltipOpts(trigger='item'),
                            title_opts=opts.TitleOpts(title = title,pos_left='center'),
                            legend_opts=opts.LegendOpts(pos_top='5%',
                                                        textstyle_opts=opts.TextStyleOpts(color='auto'),  # 文字样式
                                                        ),
                            )
           )
    return pie
# 绘制某一个属性前多少的柱形图
def draw_single_bar(data,itemstyle_bar,data_score,top,title):
    data_pair = generated_data.get_one_top(data,data_score,top)
    bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK,),)
    .add_xaxis([i[0] for i in data_pair])
    .add_yaxis(series_name=f'TOP{top}{data_score}', y_axis=[i[1] for i in data_pair],
               label_opts=opts.LabelOpts(position='top', formatter='{c}辆',
                                         color='white', font_weight='bold'),
               itemstyle_opts=itemstyle_bar,
               category_gap='30',  ## 同一序列柱间的距离
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_left='center'),
        legend_opts=opts.LegendOpts(pos_top='5%',
                                    textstyle_opts=opts.TextStyleOpts(color='auto'),  # 文字样式
                                    ),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow',
                                      ),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(font_weight='bold', color='white',  ##粗体白色
                                          ),
        )
    )
    )
    return bar

# 绘制用tab来展示多个属性随年份变化的折线图
def draw_tab(data,data_list,year,itemstyle):
    tab = Tab()
    for i in data_list:
        data_filled = generated_data.get_two_column(data,i,'year')
        t1 = draw_timeline(year,data_filled,itemstyle)
        tab.add(t1,i)
    return tab
def draw_timeline(year,data_filled,itemstyle):
    t1 = Timeline(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    max_y = generated_data.get_max(data_filled,year)
    for i in year:
        data_pair = data_filled.iloc[:,[0,i-2010 + 1]].values.tolist()
        line = draw_line(data_pair,max_y,itemstyle)
        t1.add(line,i)
    return t1
def draw_line(data_pair,max_y,itemstyle):
    line = (Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis([ i[0] for i in data_pair])
    .add_yaxis("", [ i[1] for i in data_pair],
               is_symbol_show=False, is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               markline_opts=opts.MarkLineOpts(data=[
                   opts.MarkLineItem(type_='average', name='均值线', ),
                   opts.MarkLineItem(type_='max', name='最大值线', ),
                   opts.MarkLineItem(type_='min', name='最小值线', ),
               ], ),
               markpoint_opts=opts.MarkPointOpts(data=[
                   opts.MarkPointItem(type_='average', name='均值点', ),
                   opts.MarkPointItem(type_='max', name='最大值点', ),
                   opts.MarkPointItem(type_='min', name='最小值点', ),
               ]),
               itemstyle_opts=itemstyle)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=False), ),
        yaxis_opts=opts.AxisOpts(
            max_= max_y,  # 设置y轴最大值
            splitline_opts=opts.SplitLineOpts(is_show=False),  # 去掉y轴网格线
        ),
        legend_opts=opts.LegendOpts(is_show=False)
    )
    )
    return line

#每一年各品牌的平均价格
def draw_price_average(year,data_pair,itemstyle_line):
    tab = Tab()
    max_y = max([i[2] for i in data_pair])
    for y in year:
        dp = [[j[1], j[2]] for j in data_pair if j[0] == y]
        line = draw_line(dp,max_y,itemstyle_line)
        tab.add(line, y)
    return tab

# 绘制单变量柱形图
def draw_bar(data_pair,bar_style,title,single1,single2):
    bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK,width='800px'))
    .add_xaxis([i[0] for i in data_pair])
    .add_yaxis(single2, [i[1] for i in data_pair],
               itemstyle_opts=bar_style,
               label_opts=opts.LabelOpts(position='top', font_weight='bold', color='aotu',
                                         formatter="{c}辆",
                                         )
               )
    .set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_left='center'),
        legend_opts=opts.LegendOpts(pos_top='5%'),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'),
        xaxis_opts=opts.AxisOpts(name=single1, name_location='center', name_gap=40,
                                 name_textstyle_opts=opts.TextStyleOpts(font_weight='bold', color='orange'),
                                 axisline_opts={'show': True, "lineStyle": {'color': 'orange', "width": 2}},
                                 axistick_opts={'show': False},
                                 axislabel_opts={'color': 'orange'},
                                 splitline_opts={'show': False}
                                 ),
        yaxis_opts=opts.AxisOpts(name=single2, name_location='center', name_gap=50,
                                 name_textstyle_opts=opts.TextStyleOpts(font_weight='bold', color='orange'),
                                 axisline_opts={'show': True, "lineStyle": {'color': 'cyan', "width": 2}},
                                 axistick_opts={'show': False},
                                 axislabel_opts={'color': 'orange'},
                                 splitline_opts={'show': False}
                                 )

    )
    )
    return bar

#用plot绘制
def plot_vehicle_data(data, x='行驶距离(万公里)',
        y='price',hue='车辆级别'):
    fig, axs = plt.subplots(1, 2, figsize=(15, 5), dpi=100, gridspec_kw=dict(width_ratios=[4, 2]))
    sns.scatterplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        ax=axs[0]
    )
    axs[0].set_title(f'{x}与{y}的关系')
    sns.histplot(
        data=data,
        x=x,
        hue=hue,
        shrink=0.5,
        ax=axs[1]
    )
    axs[1].set_title(f'不同{hue}的行驶距离分布')
    plt.tight_layout()  # 调整子图之间的间距
    return plt

#绘制用tab展示每一年上牌时间间隔
def get_data6(data, year,data_score='上牌时间间隔',):
    data['上牌时间'] = pd.to_datetime(data['上牌时间'])
    tab = Tab()
    for i in year:
        def calculate_time_interval(row):
            if row['上牌时间'].year > i:
                return '未上牌'
            else:
                return str(i - row['上牌时间'].year)

        data['上牌时间间隔'] = data.apply(calculate_time_interval, axis=1)
        df = data.groupby('上牌时间间隔').size().reset_index(name='count').values.tolist()
        pie = (Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(series_name='上牌时间间隔', data_pair=df,
             radius=['20%', '40%'], center=['50%', '50%'], rosetype='area',
             label_opts=opts.LabelOpts(formatter='{b},{c}\n百分占比{d}%'), )  # 标签配置)
        .set_global_opts(title_opts=[
            dict(text='上牌时间间隔', top=0, left='center'),

        ], legend_opts=opts.LegendOpts(pos_top='7%'))

        )

        tab.add(pie, str(i))
    return tab

def draw_bar1(data,itemstyle,itemstyle1):
    dp3 = data.groupby('车辆级别')['行驶距离(万公里)'].sum().reset_index()
    dp4 = data.groupby('车辆级别')['price'].mean().reset_index()
    dp4['price'] = dp4['price'].round(2)
    dp5 = pd.merge(dp3, dp4, on='车辆级别').values.tolist()

    bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color='#080b30',width='800px'))
           .add_xaxis([i[0] for i in dp5])
           .add_yaxis('行驶距离（万公里）', [i[1] for i in dp5], yaxis_index=0,
                      itemstyle_opts=itemstyle, )
           .add_yaxis('平均价格', [i[2] for i in dp5], yaxis_index=1,
                      itemstyle_opts=itemstyle1)
           .extend_axis(
        yaxis=opts.AxisOpts(
            name='平均价格', interval=10, ))
           .set_global_opts(
        title_opts=opts.TitleOpts(title='不同车辆级别基本情况对比', pos_left='center'),
        xaxis_opts=opts.AxisOpts(splitline_opts={'show': False}),
        yaxis_opts=opts.AxisOpts(name='行驶距离（万公里）', splitline_opts={'show': False}),
        legend_opts=opts.LegendOpts(pos_top='7%'),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
    )
           .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
           )
    return bar

#绘制可视化分析图集
def draw_album(data,):
    fig, axes = plt.subplots(2, 3, figsize=(16, 17))
    sns.boxplot(x='车辆级别', y='price', data=data, ax=axes[0, 0])
    axes[0, 0].tick_params(axis='x', rotation=90)
    sns.boxplot(x='车身颜色', y='price', data=data, ax=axes[0, 1])
    axes[0, 1].tick_params(axis='x', rotation=90)
    sns.boxplot(x='驱动方式', y='price', data=data, ax=axes[0, 2])
    axes[0, 2].tick_params(axis='x', rotation=90)
    plt.title('箱线图', fontsize=16, y=2.22, x=-0.1)
    sns.lineplot(x='行驶距离(万公里)', y='price', data=data, ax=axes[1, 1])
    axes[1, 1].set_title('行驶距离与价格的折线图')
    sns.histplot(data['price'], bins=10, kde=False, ax=axes[1, 0])
    axes[1, 0].set_title('价格的直方图')
    # # 热力图
    data_pair = data[['price', '行驶距离(万公里)', 'year']].corr().round(2)
    sns.heatmap(data_pair, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=axes[1, 2]).set_title('    热力图')
    return plt

#绘制保险分布饼图
def get_insurance_pie(data, data_score='年检到期'):
    data[data_score] = pd.to_datetime(data[data_score])
    year = data['year'].unique().tolist()
    year = sorted(year)
    tab = Tab()
    for i in year:
        def calculate_time_interval(row):
            if row[data_score].year > i:
                return f"{data_score[:2]}未过期"
            else:
                return str(i - row[data_score].year) + '年'

        data[f'{data_score}间隔'] = data.apply(calculate_time_interval, axis=1)
        df = data.groupby(f'{data_score}间隔').size().reset_index(name='count').values.tolist()
        pie = (Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(series_name=f'{data_score}间隔', data_pair=df,
             radius=['20%', '40%'], center=['50%', '50%'], rosetype='area',
             label_opts=opts.LabelOpts(formatter='{b},{c}\n百分占比{d}%'), )  # 标签配置)
        .set_global_opts(title_opts=[
            dict(text=f'{data_score}间隔', top=0, left='center'),

        ], legend_opts=opts.LegendOpts(pos_top='7%'))

        )

        tab.add(pie, str(i) + '年')
    return tab
# 趋势分析
def plot_trend_analysis(data):
    plt.figure(figsize=(10, 6))
    plt.hist(data['上牌时间'], bins=12, alpha=0.5, label='上牌时间')
    plt.hist(data['年检到期'], bins=12, alpha=0.5, label='年检到期')
    plt.hist(data['保险到期'], bins=12, alpha=0.5, label='保险到期')
    plt.legend()
    plt.title('上牌时间、年检到期和保险到期分布')
    plt.xlabel('日期')
    plt.ylabel('车辆数量')
    return plt
def analyze_intervals(df):
    # 计算年检和保险与上牌时间的间隔
    df['年检间隔'] = (df['年检到期'] - df['上牌时间']).dt.days
    df['保险间隔'] = (df['保险到期'] - df['上牌时间']).dt.days

    # 创建一个图形和两个子图，设置为横着排列（1行2列）
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # 绘制年检间隔的直方图
    ax1.hist(df['年检间隔'], bins=50, alpha=0.5, color='blue', label='年检间隔')
    ax1.set_title('年检与上牌时间的间隔')
    ax1.set_xlabel('天数')
    ax1.set_ylabel('车辆数量')
    ax1.legend()

    # 绘制保险间隔的直方图
    ax2.hist(df['保险间隔'], bins=50, alpha=0.5, color='green', label='保险间隔')
    ax2.set_title('保险与上牌时间的间隔')
    ax2.set_xlabel('天数')
    ax2.set_ylabel('车辆数量')
    ax2.legend()

    plt.tight_layout()
    return plt

def analyze_vehicle_expiration(df):
    # 异常值分析
    # 找出年检或保险已经过期的车辆
    expired_inspection = df[df['年检到期'] < pd.Timestamp('today')]
    expired_insurance = df[df['保险到期'] < pd.Timestamp('today')]
    # 绘制散点图，查看上牌时间与年检、保险到期的关系
    plt.figure(figsize=(10, 6))
    plt.scatter(df['上牌时间'], df['年检到期'], c='blue', label='年检到期', alpha=0.5)
    plt.scatter(df['上牌时间'], df['保险到期'], c='red', label='保险到期', alpha=0.5)
    plt.legend()
    plt.title('上牌时间与年检、保险到期的关系')
    plt.xlabel('上牌时间')
    plt.ylabel('到期时间')
    return plt
#形式距离与年份变化的散点图
def draw_scatter(data):
    dp2 = data[['year', '行驶距离(万公里)']].values.tolist()
    sca = (Scatter()
        .add_xaxis([i[0] for i in dp2])
        .add_yaxis('年份', [i[1] for i in dp2],
                   label_opts=opts.LabelOpts(is_show=False), symbol_size=12)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='行驶距离与年份的变化', pos_left='center'),
            tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="cross", formatter='{c}万公里',
                                          background_color='skyblue', border_width=1),
            xaxis_opts=opts.AxisOpts(name='年'),
            yaxis_opts=opts.AxisOpts(name='行驶距离(万公里)'),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=20, is_show=True),
        )
    )
    return sca

def bar_over_line(data):
    dp1 = data.groupby('year').agg({'title': 'count', '行驶距离(万公里)': 'mean'}).reset_index().values.tolist()
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='800px'))
    bar.add_xaxis([i[0] for i in dp1])
    bar.add_yaxis('车辆数量', [i[1] for i in dp1], yaxis_index=0,
                  itemstyle_opts=itemsyle_all.itemstyle2,
                  label_opts=opts.LabelOpts(formatter='{c}辆', color='auto')
                  )
    bar.extend_axis(
        yaxis=opts.AxisOpts(name='平均行驶距离(万公里)', position='right',
                            axislabel_opts=opts.LabelOpts(formatter="{value}"),
                            splitline_opts=opts.SplitLineOpts(is_show=False),
                            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color='black')))
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title='不同年份车辆数量与平均行驶距离', pos_left='center', pos_top='5%'),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
        legend_opts=opts.LegendOpts(pos_top='10%'),
        xaxis_opts=opts.AxisOpts(name='年份', splitline_opts={'show': False}, name_location='middle', name_gap=26,
                                 axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color='black'))),
        yaxis_opts=opts.AxisOpts(
            name='车辆数量',
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color='black'))
        )
        )
    line = (Line()
            .add_xaxis([i[0] for i in dp1])
            .add_yaxis("平均行驶距离(万公里)", [i[2] for i in dp1], yaxis_index=1, z_level=2,
                       itemstyle_opts=itemsyle_all.itemstyle1,
                       is_smooth=True, is_symbol_show=False, linestyle_opts=opts.LineStyleOpts(width=2, opacity=0.8)
                       )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            )

    bar.overlap(line)
    return bar
def draw_line2(data):
    data['上牌时间'] = pd.to_datetime(data['上牌时间'])
    data['年检到期'] = pd.to_datetime(data['年检到期'])
    data['保险到期'] = pd.to_datetime(data['保险到期'])
    line = (Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='800px'))
    .add_xaxis(data['上牌时间'].dt.strftime('%Y-%m-%d').tolist())
    .add_yaxis("上牌时间", data['上牌时间'].tolist(), is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False))
    .add_xaxis(data['年检到期'].dt.strftime('%Y-%m-%d').tolist())
    .add_yaxis("年检到期", data['年检到期'].tolist(), is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False))
    .add_xaxis(data['保险到期'].dt.strftime('%Y-%m-%d').tolist())
    .add_yaxis("保险到期", data['保险到期'].tolist(), is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='随时间变化，上牌时间，年检到期时间，保险到期时间的变化', pos_top='5%'),
        tooltip_opts=opts.TooltipOpts(trigger='axis'),
        xaxis_opts=opts.AxisOpts(type_='time'),
        yaxis_opts=opts.AxisOpts(type_='time'),
        datazoom_opts=[opts.DataZoomOpts()],
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    ))
    return line

def draw_word_cloud(data):
    plt.figure(figsize=(8, 6))
    brand_counts = data['brands'].value_counts().reset_index(name='频率')
    b = brand_counts.round(2)
    wordcloud = (WordCloud()
    .add('品牌', b.values.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title='车辆品牌词云图', pos_left='center'),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    ))
    return wordcloud