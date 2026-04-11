import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

# ================= 页面设置 =================
st.set_page_config(
    page_title="中医体质分析",
    page_icon="🩺",
    layout="centered"
)

# ================= CSS美化 =================
st.markdown("""
<style>
.big-title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    color: #2E7D32;
    margin-bottom: 10px;
}

.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f5f7fa;
    margin-bottom: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}

.result-box {
    padding: 15px;
    border-radius: 12px;
    background-color: #e8f5e9;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🩺 中医体质分析系统</div>", unsafe_allow_html=True)

# ================= 评分说明 =================
with st.expander("📝 评分说明（点击展开）"):
    st.write("""
    1 = 从不  
    2 = 很少  
    3 = 有时  
    4 = 经常  
    5 = 总是
    """)

# ================= 题库 =================
QUESTIONS = [
    {"q": "你是否容易感到疲劳？", "type": "气虚"},
    {"q": "你是否怕冷？", "type": "阳虚"},
    {"q": "你是否口干？", "type": "阴虚"},
    {"q": "你是否身体困重？", "type": "痰湿"},
    {"q": "你是否容易长痘？", "type": "湿热"},
    {"q": "你是否有刺痛感？", "type": "血瘀"},
    {"q": "你是否情绪压抑？", "type": "气郁"},
    {"q": "你是否容易过敏？", "type": "特禀"},
    {"q": "你是否精力充沛？", "type": "平和"},
]

# ================= 选项 =================
options = {"从不": 1, "很少": 2, "有时": 3, "经常": 4, "总是": 5}

answers = []

st.subheader("📋 请完成问卷")

for i, item in enumerate(QUESTIONS, 1):
    with st.container():
        st.markdown(f"<div class='card'><b>{i}. {item['q']}</b></div>", unsafe_allow_html=True)

        choice = st.radio("", list(options.keys()), key=i, horizontal=True)
        answers.append((item["type"], options[choice]))

# ================= 计算 =================
def calculate(answers):
    raw = {}
    count = {}

    for t, v in answers:
        raw[t] = raw.get(t, 0) + v
        count[t] = count.get(t, 0) + 1

    result = {}

   