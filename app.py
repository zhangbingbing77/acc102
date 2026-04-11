import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面标题
st.title("ACC102 Track4 数据可视化小工具")

# 上传文件
uploaded_file = st.file_uploader("上传CSV或Excel数据", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 读取数据
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    # 显示数据
    st.subheader("数据预览")
    st.dataframe(df)

    # 简单图表
    st.subheader("数据分布图表")
    plt.hist(df.iloc[:, -1], bins=10)  # 取最后一列画图
    st.pyplot(plt)