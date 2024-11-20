
import streamlit as st
import pandas as pd
import sweetviz as sv
from streamlit.components.v1 import html

# 初始化Streamlit会话状态
def dataeda():
    if 'uploaded_file' not in st.session_state:  # 上传文件
        st.session_state['uploaded_file'] = None
    if 'report_generated' not in st.session_state:  # 生产报告状态
        st.session_state['report_generated'] = False
    if 'report_content' not in st.session_state:  # 报告内容状态
        st.session_state['report_content'] = None
    # 初始化Streamlit会话状态
    if 'uploaded_file_name' not in st.session_state:  # 上传文件状态
        st.session_state['uploaded_file_name'] = None

    def create_report(filename):
        data_source = pd.read_csv(filename, encoding='utf-8')
        st.success('报告生成中,请等待!')
        report = sv.analyze(data_source)
        report.show_html('report.html', open_browser=False, layout='vertical', scale=1.0)
        st.success('报告生成完毕,点击查看报告查阅报告!')

    def show_report():
        st.success('数据分析报告已生成!具体内容如下:')
        with open('report.html', 'r', encoding='utf-8') as f:
            st.session_state['report_content'] = f.read()
            html(st.session_state['report_content'], scrolling=True, width=1000, height=1200)

    _, col2, _ = st.columns([0.15, 0.7, 0.15])

    with col2:
        uploaded_file = st.file_uploader(
            "你可以选择性上传一个CSV文件",
            type=['csv'],
            accept_multiple_files=False
        )
        uploaded_file_name = None
        if uploaded_file is not None:
            uploaded_file_name = uploaded_file.name
        left, middle1, middle2, right = st.columns(4, gap='large')
        # 先检测文件是否存在,文件存在用户可以点击查看文件内容,
        if left.button("点击查看文件"):
            if uploaded_file is not None:
                st.success('文件已上传成功!文件内容如下:', icon="✅")
                data = pd.read_csv(uploaded_file, encoding='utf-8')
                st.dataframe(data)
            else:
                st.error("你没有上传任何文件", icon="🚨")

        generate_report_button = middle1.button('生成数据报告')

        # 如果用户点击了生成报告按钮，并且有上传的文件
        if generate_report_button and uploaded_file is not None:
            st.info('检测到上传的文件存在,现在开始生成数据分析报告...')
            create_report(uploaded_file)
            st.session_state['uploaded_file_name'] = uploaded_file_name
            st.session_state['report_generated'] = True
            st.session_state['uploaded_file'] = uploaded_file  # 更新上传文件状态
        elif generate_report_button and uploaded_file is None:
            st.error('请先上传文件，然后再点击生成数据分析报告按钮。')
            st.session_state['report_generated'] = False

        show_report_button = middle2.button('查看数据报告')

        if show_report_button:
            # st.info('你点击量查看报告')
            print('触发测试', st.session_state['report_generated'])
            if uploaded_file is None:
                print('触发测试具体', st.session_state['uploaded_file'])
                st.error('检测到未上传文件，请先上传文件')
            elif uploaded_file is not None and st.session_state['report_generated'] is False:
                st.error('检测到未点击报告生 成按钮，请先点击生成数据分析报告按钮')
            elif uploaded_file is not None and uploaded_file_name != st.session_state['uploaded_file_name']:
                st.error('检测到上传文件发生变化，请重新生成数据分析报告')
            else:
                show_report()
                button_right = right.download_button(
                    label='下载数据报告',
                    use_container_width=True,
                    data=st.session_state['report_content'].encode('utf-8'),
                    file_name='data_analysis_report.html',
                )
                if button_right:
                    st.info('数据分析报告下载完成!欢迎再次使用')


if __name__ == "__main__":
    run_code = 0
