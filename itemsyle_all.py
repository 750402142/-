
from pyecharts.commons.utils import JsCode
pie_style = {
    'normal': {
        'borderRadius': 10,
        'borderWidth': .5,
        'borderColor': 'auto',
    }
}

line_itemstyle1 =  {"normal": {
    "shadowColor": 'rgba(0, 6, 9, .3)',
    "shadowBlur": 5,
    "shadowOffsetY": 2,
    "shadowOffsetX": 2,
    "width": 2}}
itemstyle_line = {
    'normal': {
        'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: 'rgb(255, 191, 0)' },
          { offset: 1, color: 'rgb(224, 62, 76)' }
        ],)"""),
        'lineStyle': {
            'width': 2,
            'type': 'solid',
            'shadowColor': 'rgba(108, 80, 243, 0.9)',  # 线条阴影的颜色
            'shadowBlur': 5,  # 线条阴影的宽度
        },
        'areaStyle': {
            'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 1, 1, [
             { offset: 0, color: 'rgba(255, 191, 0, 0.3)' },
             { offset: 1, color: 'rgba(224, 62, 76, 0.3)' }
           ],)"""),
            'opacity': 0.5
        }
    }
}
bar_style = {"normal": {
    'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 1, 1, [
            { offset: 0, color: '#80beb0' },
            { offset: 0.2, color: '#b3ddd1' },
            { offset: 0.4, color: '#80beb0' },
            { offset: 0.6, color: '#d2dce2' },
            { offset: 0.8, color: '#f5b995' },
            { offset: 1, color: '#ed9c6c' },
            ],)"""),
    "shadowColor": 'rgba(0, 0, 0, .3)',
    "shadowBlur": 5,
    "shadowOffsetY": 2,
    "shadowOffsetX": 2,
    "barBorderRadius": [4, 4, 4, 4],
    "width": 2}}

itemstyle_bar = {
        'normal': {
            'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(255, 191, 0)' },
              { offset: 1, color: 'rgb(224, 62, 76)' }
            ],)"""),
            'barBorderRadius': [10, 10, 10, 10],  # 柱子的四个角圆角设计
            'shadowColor': 'rgba(108,80,243,0.9)',  # 阴影的颜色
            'shadowBlur': 20,  # 阴影的宽度
        }
    }
itemstyle1_bar1 = {
        'normal': {
            'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(128, 255, 165)' },
              { offset: 1, color: 'rgb(1, 191, 236)' }
            ],)"""),
            'barBorderRadius': [10, 10, 10, 10],  # 柱子的四个角圆角设计
            'shadowColor': 'rgba(108,80,243,0.9)',  # 阴影的颜色
            'shadowBlur': 20,  # 阴影的宽度
        }
    }

itemstyle2 = {
    'normal': {
        'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: 'rgb(40, 141, 125)' },
          { offset: 1, color: 'rgb(199, 229, 227)' }
        ],)"""),
        'barBorderRadius': [20,20,20,20],      #  柱子的四个角圆角设计
        'shadowColor':'rgba(108,80,243,0.9)', # 阴影的颜色
        'shadowBlur':5, # 阴影的宽度
        'width': 4,
    }
}
itemstyle1 = {
    'normal': {
        'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {offset: 0, color: 'rgba(255, 0, 0, 1)'},
            {offset: 1, color: 'rgba(0, 255, 0, 1)'}
        ], false)"""),
        'lineStyle': {
            'width': 4,
            'type': 'solid',
            'color': JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: 'rgba(255, 0, 0, 0.5)'},
                {offset: 1, color: 'rgba(0, 255, 0, 0.5)'}
            ], false)"""),
        },
        'borderColor': 'rgba(0, 0, 0, 0.5)',
        'borderWidth': 8,
        'shadowColor': 'rgba(0, 0, 0, 0.4)',
        'shadowBlur': 10,
        'shadowOffsetY': 10,
    }
}
