# filename: tcm_constitution_app_export.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json, os

# -------------------------
# 题目和体质分类
# -------------------------
questions = {
    "平和质": [
        "你精力充沛吗？",
        "你睡眠良好吗？",
        "你食欲正常吗？",
        "你适应环境能力强吗？"
    ],
    "气虚质": [
        "你容易疲劳吗？",
        "你说话声音低弱吗？",
        "你容易出虚汗吗？",
        "你容易心慌吗？"
    ],
    "阳虚质": [
        "你手脚发凉吗？",
        "你怕冷吗？",
        "你吃凉的会腹泻吗？"
    ],
    "阴虚质": [
        "你容易口干吗？",
        "你手脚心发热吗？",
        "你容易失眠吗？"
    ],
    "痰湿质": [
        "你体型偏胖吗？",
        "你容易困倦吗？",
        "你嘴里发黏吗？"
    ],
    "湿热质": [
        "你面部容易出油吗？",
        "你口苦吗？",
        "你大便黏滞吗？"
    ],
    "血瘀质": [
        "你有身体刺痛感吗？",
        "你肤色晦暗吗？",
        "你容易有黑眼圈吗？"
    ],
    "气郁质": [
        "你容易情绪低落吗？",
        "你容易焦虑吗？",
        "你爱叹气吗？"
    ],
    "特禀质": [
        "你容易过敏吗？",
        "你对气味敏感吗？",
        "你没感冒也打喷嚏吗？",
        "你皮肤易起荨麻疹吗？"
    ]
}

# -------------------------
# Streamlit 页面设置
# -------------------------
st.set_page_config(page_title="中医体质自测", layout="wide")
st.title("中医体质自测问卷")
st.write("请根据自己的情况打分：1=完全不符合，5=完全符合")

# -------------------------
# 用户评分输入
# -------------------------
scores = {}
for constitution, qs in questions.items():
    st.subheader(constitution)
    scores[constitution] = []
    for q in qs:
        score = st.slider(q, 1, 5, 3)
        scores[constitution].append(score)

# -------------------------
# 计算体质百分比
# -------------------------
if st.button("计算体质倾向"):
    percentages = {}
    for constitution, values in scores.items():
        max_score = 5 * len(values)
        percentages[constitution] = round(sum(values)/max_score*100, 1)

    st.subheader("各体质倾向百分比")
    st.write(percentages)

    # -------------------------
    # 绘制雷达图
    # -------------------------
    categories = list(percentages.keys())
    values = list(percentages.values())
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2, label="体质倾向")
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 100)
    ax.set_title("中医体质雷达图", va='bottom')
    st.pyplot(fig)

    # -------------------------
    # 保存记录
    # -------------------------
    if not os.path.exists("records"):
        os.mkdir("records")
    record = {"scores": scores, "percentages": percentages}
    record_file = "records/record.json"
    with open(record_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    st.success("测试记录已保存！")

    # -------------------------
    # 导出 Excel
    # -------------------------
    df_scores = []
    for c, q_list in scores.items():
        for i, q in enumerate(questions[c]):
            df_scores.append({"体质类型": c, "题目": q, "分数": q_list[i]})
    df_scores = pd.DataFrame(df_scores)

    # 百分比单独表格
    df_percent = pd.DataFrame(list(percentages.items()), columns=["体质类型", "百分比"])

    with pd.ExcelWriter("records/record.xlsx") as writer:
        df_scores.to_excel(writer, index=False, sheet_name="原始打分")
        df_percent.to_excel(writer, index=False, sheet_name="体质百分比")
    st.success("测试记录已导出为 Excel！")
    st.download_button("下载 Excel 文件", "records/record.xlsx", "record.xlsx")