import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

st.title("🩺 中医体质测试")

# ===== 30题 中医体质测试题库 =====
QUESTIONS = [
    # 平和质 4题
    {"q": "你精力充沛吗？", "type": "平和"},
    {"q": "你睡眠良好吗？", "type": "平和"},
    {"q": "你食欲正常吗？", "type": "平和"},
    {"q": "你适应环境能力强吗？", "type": "平和"},

    # 气虚质 4题
    {"q": "你容易疲劳吗？", "type": "气虚"},
    {"q": "你说话声音低弱吗？", "type": "气虚"},
    {"q": "你容易出虚汗吗？", "type": "气虚"},
    {"q": "你容易心慌吗？", "type": "气虚"},

    # 阳虚质 3题
    {"q": "你手脚发凉吗？", "type": "阳虚"},
    {"q": "你怕冷吗？", "type": "阳虚"},
    {"q": "你吃凉的会腹泻吗？", "type": "阳虚"},

    # 阴虚质 3题
    {"q": "你容易口干吗？", "type": "阴虚"},
    {"q": "你手脚心发热吗？", "type": "阴虚"},
    {"q": "你容易失眠吗？", "type": "阴虚"},

    # 痰湿质 3题
    {"q": "你体型偏胖吗？", "type": "痰湿"},
    {"q": "你容易困倦吗？", "type": "痰湿"},
    {"q": "你嘴里发黏吗？", "type": "痰湿"},

    # 湿热质 3题
    {"q": "你面部容易出油吗？", "type": "湿热"},
    {"q": "你口苦吗？", "type": "湿热"},
    {"q": "你大便黏滞吗？", "type": "湿热"},

    # 血瘀质 3题
    {"q": "你有身体刺痛感吗？", "type": "血瘀"},
    {"q": "你肤色晦暗吗？", "type": "血瘀"},
    {"q": "你容易有黑眼圈吗？", "type": "血瘀"},

    # 气郁质 3题
    {"q": "你容易情绪低落吗？", "type": "气郁"},
    {"q": "你容易焦虑吗？", "type": "气郁"},
    {"q": "你爱叹气吗？", "type": "气郁"},

    # 特禀质 4题
    {"q": "你容易过敏吗？", "type": "特禀"},
    {"q": "你对气味敏感吗？", "type": "特禀"},
    {"q": "你没感冒也打喷嚏吗？", "type": "特禀"},
    {"q": "你皮肤易起荨麻疹吗？", "type": "特禀"},
]

# ===== 答题 =====
answers = []
st.write("请打分（1=完全不符合，5=完全符合）")

for item in QUESTIONS:
    val = st.slider(item["q"], 1, 5, 3)
    answers.append((item["type"], val))

# ===== 计算 =====
def calculate(answers):
    raw = {}
    count = {}

    for t, v in answers:
        raw[t] = raw.get(t, 0) + v
        count[t] = count.get(t, 0) + 1

    result = {}
    for t in raw:
        max_s = count[t] * 5
        min_s = count[t] * 1
        score = (raw[t] - min_s) / (max_s - min_s) * 100
        result[t] = round(score, 2)

    return result

# ===== 雷达图 =====
def draw_chart(result):
    labels = list(result.keys())
    values = list(result.values())

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.2)

    ax.set_thetagrids(angles[:-1]*180/np.pi, labels)

    return fig

# ===== 保存 =====
def save(result):
    os.makedirs("data", exist_ok=True)
    file = "data/history.json"

    try:
        with open(file, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "time": datetime.now().isoformat(),
        "result": result
    })

    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ===== 按钮 =====
if st.button("生成结果"):

    result = calculate(answers)

    st.subheader("📊 体质百分比")
    for k, v in result.items():
        st.write(f"{k}: {v}%")

    st.subheader("📈 雷达图")
    fig = draw_chart(result)
    st.pyplot(fig)

    save(result)

    st.success("已保存")
   