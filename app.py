import pickle

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

from networkx import read_multiline_adjlist
from streamlit.components.v1 import html

from streamlit_option_menu import option_menu
from matplotlib import pyplot as plt
from pyecharts.charts import Page
import seaborn as sns
import creat #这是有绘制各种图形函数的类
import generated_data as gd #这是来生成图形的类
import itemsyle_all as item #这是

import streamlit as st
st.set_page_config(layout="wide")
data = pd.read_csv("./data/二手车上牌数据处理.csv")
data1 = pd.read_csv('./data/二手车未上牌.csv')

with open('./data/info.txt','r',encoding='utf-8') as f:
    infos = f.read()
def read_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data
def read_figure(filepath):
    with open(filepath,'rb') as f:
        fig = pickle.loads(f.read())
    return fig
with st.sidebar:
    selected = option_menu(
        menu_title='车辆二手车数据分析',  # required
        options=["Home",'基本信息查询', '主要考虑因素','二手车可视化分析','时间信息前端可视化概览图'],  # 每个选项的名称
        icons=["house", "list-ul", "chat", "bar-chart", "clock"],
        menu_icon="browser-firefox",  # 标题旁边的图标
        default_index=0,  # optional
        orientation="vertical",  # 布局是垂直方向
        styles={
            "container": {"padding": "5!important", "background-color": "#d3e3fd"},  # 调整整个菜单的Div容器
            "icon": {"color": "orange", "font-size": "22px"},  # 调整图标的样式
            "nav-link": {"font-size": "16px", "font-weight": "bold", "color": "black"},   # 每个选项文本的样式
            "nav-link-selected": {"background-color": "#ffc473", "color": "red"},  # 选中选项的样式
        }
    )

if selected == "Home":
    st.markdown(body='# <div style="text-align: center; color: #ff0000;">车辆二手车数据分析</div>',unsafe_allow_html=True)
    left, right = st.columns([0.6, 0.4], gap='large')
    with left:
        st.markdown(infos)
        html(read_html('./result/所有品牌的词云图.html'), height=800)
    with right:
        st.image('./data/封面.jpg')
if selected == "Home":
    with st.sidebar:
        selected_sub = option_menu(
            key='cat',
            menu_title=None,
            options=['小组: 第四组', "项目名称:车辆二手车数据分析"],
            icons=["users", "clipboard-data"],
            menu_icon="browser-firefox",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5!important", "background-color": "#ffffff"},
                "icon": {"color": "orange", "font-size": "16px"},
                "nav-link": {"font-size": "16px", "font-weight": "bold", "color": "black"},
                "nav-link-selected": {"background-color": "#dfe7f7", "color": "orange"},
            }
        )
elif selected == '基本信息查询':
    with st.sidebar:
        selected = option_menu(
            menu_title='基本信息查询',  # required
            options=['未上牌的车辆基本信息', '上牌车辆信息'],  # 每个选项的名称
            icons=["car-front", "car-front"],  # 每个选项的图标
            menu_icon="search",  # 标题旁边的图标，这里改为了表示搜索的图标，更贴合查询信息的情境
            default_index=0,  # optional
            orientation="vertical",  # 布局是垂直方向
            styles={
                "container": {"padding": "5!important", "background-color": "#d3e3fd"},  # 调整整个菜单的Div容器
                "icon": {"color": "orange", "font-size": "22px"},  # 调整图标的样式
                "nav-link": {"font-size": "16px", "font-weight": "bold", "color": "black"},  # 每个选项文本的样式
                "nav-link-selected": {"background-color": "#ffc473", "color": "red"},  # 选中选项的样式
            }
        )
    if selected == '未上牌的车辆基本信息':
        st.dataframe(data1)
    elif selected == '上牌车辆信息':

        # 读取数据
        df = pd.read_csv('./data/二手车上牌数据处理.csv')

        # 创建 Streamlit 应用
        st.title('车辆筛选器')
        # 选择品牌
        selected_brands = st.multiselect('选择品牌', df['brands'].unique(), [])  # 默认不选择任何品牌
        # 选择价格范围
        price_min_set = st.checkbox('设置最低价格')  # 添加一个复选框来检查用户是否想要设置最低价格
        price_max_set = st.checkbox('设置最高价格')  # 添加一个复选框来检查用户是否想要设置最高价格
        price_min = st.number_input('最低价格', min_value=df['price'].min(), max_value=df['price'].max(),
                                    value=None) if price_min_set else None
        price_max = st.number_input('最高价格', min_value=df['price'].min(), max_value=df['price'].max(),
                                    value=None) if price_max_set else None
        # 选择行驶里程范围
        odometer_min_set = st.checkbox('设置最低行驶里程')  # 添加一个复选框来检查用户是否想要设置最低行驶里程
        odometer_max_set = st.checkbox('设置最高行驶里程')  # 添加一个复选框来检查用户是否想要设置最高行驶里程
        odometer_min = st.number_input('最低行驶里程 (万公里)', min_value=df['行驶距离(万公里)'].min(),
                                       max_value=df['行驶距离(万公里)'].max(),
                                       value=None) if odometer_min_set else None
        odometer_max = st.number_input('最高行驶里程 (万公里)', min_value=df['行驶距离(万公里)'].min(),
                                       max_value=df['行驶距离(万公里)'].max(),
                                       value=None) if odometer_max_set else None
        # 选择车辆级别
        selected_vehicle_levels = st.multiselect('选择车辆级别', df['车辆级别'].unique(), [])  # 默认不选择任何级别
        # 构建过滤条件
        filter_conditions = []
        if selected_brands:
            filter_conditions.append(df['brands'].isin(selected_brands))
        if price_min is not None:
            filter_conditions.append(df['price'] >= price_min)
        if price_max is not None:
            filter_conditions.append(df['price'] <= price_max)
        if odometer_min is not None:
            filter_conditions.append(df['行驶距离(万公里)'] >= odometer_min)
        if odometer_max is not None:
            filter_conditions.append(df['行驶距离(万公里)'] <= odometer_max)
        if selected_vehicle_levels:
            filter_conditions.append(df['车辆级别'].isin(selected_vehicle_levels))
        # 如果没有设置任何筛选条件，则显示所有数据
        if not filter_conditions:
            filtered_df = df.copy()
        else:
            # 使用所有筛选条件来过滤 DataFrame
            filtered_df = df[filter_conditions[0]]
            for condition in filter_conditions[1:]:
                filtered_df = filtered_df[condition]
        # 显示筛选后的表格数据
        st.write('筛选后的车辆数据:')
        if filtered_df.shape[0] == 0:
            st.warning('暂无符合该条件的车辆,请重新选择!')
        else:
            st.table(filtered_df.iloc[:, 1:])
elif selected == '主要考虑因素':
    with st.sidebar:
        selected = option_menu(
            menu_title='主要考虑因素',  # required
            options=['主要考虑因素近几年静态分析','主要考虑因素近几年动态分析'],  # 每个选项的名称
            icons=["bar-chart-steps", "bar-chart-steps"],  # 每个选项的图标
            menu_icon="browser-firefox",  # 标题旁边的图标
            default_index=0,  # optional
            orientation="vertical",  # 布局是垂直方向
            styles={
                "container": {"padding": "5!important", "background-color": "#d3e3fd"},  # 调整整个菜单的Div容器
                "icon": {"color": "orange", "font-size": "22px"},  # 调整图标的样式
                "nav-link": {"font-size": "16px", "font-weight": "bold", "color": "black"},  # 每个选项文本的样式
                "nav-link-selected": {"background-color": "#ffc473", "color": "red"},  # 选中选项的样式
            }
        )

    if selected =='主要考虑因素近几年动态分析':
        html(read_html('./result/tab展示各年变量的变化.html'),height=800)
    elif selected == '主要考虑因素近几年静态分析':
        left, right = st.columns([0.5, 0.5], gap='large')
        with left:
             html(read_html('result/combined_charts1.html'), height=1000)

        with right:
             html(read_html('result/combined_charts2.html'), height=1000)
elif selected == '二手车可视化分析':
    with st.sidebar:
        selected = option_menu(
            menu_title='二手车可视化分析',  # required
            options=['二手车多变量前端可视化综合分析图', '二手车数据多维度可视化分析图集','二手车价格构成前端可视化探索图'],  # 每个选项的名称
            icons=["play", "play","play"],  # 每个选项的图标
            menu_icon='./data/menu (2).svg',
            default_index=0,  # optional
            orientation="vertical",  # 布局是垂直方向
            styles={
                "container": {"padding": "5!important", "background-color": "#d3e3fd"},  # 调整整个菜单的Div容器
                "icon": {"color": "orange", "font-size": "22px"},  # 调整图标的样式
                "nav-link": {"font-size": "16px", "font-weight": "bold", "color": "black"},  # 每个选项文本的样式
                "nav-link-selected": {"background-color": "#ffc473", "color": "red"},  # 选中选项的样式
            }
        )
    if selected == '二手车多变量前端可视化综合分析图':
        left1, right1 = st.columns([0.5, 0.5], gap='large')
        with left1:
            html(read_html('result/page1.html'),height=1000)
        with right1:
            html(read_html('result/page2.html'),height=1000)
    elif selected == '二手车数据多维度可视化分析图集':
        st.title('二手车数据多维度可视化分析图集')
        st.image('result/图集.png')
    elif selected == '二手车价格构成前端可视化探索图':
        option = st.selectbox(
            "请选择你想要查看的关系",
            ('x=x=驱动方式, y=price,hue=车辆级别', '各价格区间车辆的数量',
             'x=行驶距离(万公里),y=price,hue=车辆级别','每一年各品牌的平均价格'
             ),
            index=0,
            placeholder="Select contact method...",
        )
        if option == 'x=x=驱动方式, y=price,hue=车辆级别':
            st.image('./result/x=x=驱动方式, y=price,hue=车辆级别.png')
        elif option == '各价格区间车辆的数量':
            html(read_html('./result/各价格区间的车辆.html'),height=800,width=800)# ! 这里想设置更宽更高一些,没反应,待解决
        elif option == 'x=行驶距离(万公里),y=price,hue=车辆级别':
            st.image('./result/x=行驶距离(万公里),y=price,hue=车辆级别.png')
        elif option == '每一年各品牌的平均价格':
            html(read_html('./result/每一年各品牌的平均价格.html'),height=800)
elif selected == '时间信息前端可视化概览图':
    main_selected = st.selectbox(
        "请选择你想要查看的关系",
        ('保险、年检与上牌时间的间隔',  '上牌时间、年检到期和保险到期分布', '上牌时间与年检、保险到期的关系',
         '上牌时间间隔','行驶距离与年份的变化','保险到期间隔','年检到期间隔'
         ),
        index=0,
        placeholder="Select contact method...",
    )
    if main_selected == '保险、年检与上牌时间的间隔':
        st.image('./result/保险、年检与上牌时间的间隔.png')
    elif main_selected == '上牌时间、年检到期和保险到期分布':
        st.image('./result/上课时间、年检到期和保险到期分布.png')
    elif main_selected == '上牌时间与年检、保险到期的关系':
        st.image('./result/上牌时间与年检、保险到期的关系.png')
    elif main_selected == '上牌时间间隔':
        html(read_html('./result/上牌时间间隔.html'),height=800)
    elif main_selected == '行驶距离与年份的变化':
        html(read_html('./result/行驶距离与年份的变化.html'),height=800)
    elif main_selected  == '保险到期间隔':
        html(read_html('./result/保险到期的饼图分布.html'),height=800)
    elif main_selected == '年检到期间隔':
        html(read_html('./result/年检到期的饼图分布.html'),height=800)
# elif selected == 'plot展示一些特征':
#     option = st.selectbox(
#         "请选择你想要查看的关系",
#         ('x=x=驱动方式, y=price,hue=车辆级别.png', 'x=year,y=行驶距离(万公里),hue=车辆级别.png', 'x=行驶距离(万公里),y=price,hue=车辆级别.png'),
#         index=0,
#         placeholder="Select contact method...",
#     )
#     if option == 'x=x=驱动方式, y=price,hue=车辆级别.png':
#         st.image('./result/x=x=驱动方式, y=price,hue=车辆级别.png')
#     elif option == 'x=year,y=行驶距离(万公里),hue=车辆级别.png':
#         st.image('./result/x=year,y=行驶距离(万公里),hue=车辆级别.png')
#     elif option == 'x=行驶距离(万公里),y=price,hue=车辆级别.png':
#         st.image('./result/x=行驶距离(万公里),y=price,hue=车辆级别.png')
#车辆信息的展示
import streamlit as st


