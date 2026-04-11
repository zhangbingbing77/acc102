# filename: tcm_constitution_app_with_advice.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# -------------------------
# 题目和体质分类
# -------------------------
questions = {
    "平和质": ["你精力充沛吗？", "你睡眠良好吗？", "你食欲正常吗？", "你适应环境能力强吗？"],
    "气虚质": ["你容易疲劳吗？", "你说话声音低弱吗？", "你容易出虚汗吗？", "你容易心慌吗？"],
    "阳虚质": ["你手脚发凉吗？", "你怕冷吗？", "你吃凉的会腹泻吗？"],
    "阴虚质": ["你容易口干吗？", "你手脚心发热吗？", "你容易失眠吗？"],
    "痰湿质": ["你体型偏胖吗？", "你容易困倦吗？", "你嘴里发黏吗？"],
    "湿热质": ["你面部容易出油吗？", "你口苦吗？", "你大便黏滞吗？"],
    "血瘀质": ["你有身体刺痛感吗？", "你肤色晦暗吗？", "你容易有黑眼圈吗？"],
    "气郁质": ["你容易情绪低落吗？", "你容易焦虑吗？", "你爱叹气吗？"],
    "特禀质": ["你容易过敏吗？", "你对气味敏感吗？", "你没感冒也打喷嚏吗？", "你皮肤易起荨麻疹吗？"]
}

# -------------------------
# 体质描述与建议
# -------------------------
advice = {
    "平和质": {
        "description": "体质均衡，精力充沛，适应环境能力强。",
        "suggestion": "保持健康生活习惯，均衡饮食，适度运动。"
    },
    "气虚质": {
        "description": "容易疲劳，声音低弱，出虚汗。",
        "suggestion": "注意休息，饮食温和，多进行增强体质的运动。"
    },
    "阳虚质": {
        "description": "手脚发凉，怕冷，容易腹泻。",
        "suggestion": "注意保暖，适量运动，多吃温性食物。"
    },
    "阴虚质": {
        "description": "容易口干，手脚心发热，失眠。",
        "suggestion": "避免辛辣刺激，多喝水，多吃滋阴食物。"
    },
    "痰湿质": {
        "description": "体型偏胖，困倦，口中黏腻。",
        "suggestion": "注意饮食清淡，适量运动，保持良好作息。"
    },
    "湿热质": {
        "description": "面部易出油，口苦，大便黏滞。",
        "suggestion": "饮食清淡，多喝水，注意情绪调节。"
    },
    "血瘀质": {
        "description": "肤色暗沉，有刺痛感，黑眼圈明显。",
        "suggestion": "适量运动，促进血液循环，保持心情舒畅。"
    },
    "气郁质": {
        "description": "情绪易低落，焦虑，常叹气。",
        "suggestion": "保持心情愉快，适度运动和社交，减压放松。"
    },
    "特禀质": {
        "description": "容易过敏，对气味敏感，皮肤易起荨麻疹。",
        "suggestion": "避免过敏源，注意皮肤护理，规律作息。"
    }
}

# -------------------------
# 页面设置
# -------------------------
st.set_page_config(page_title="中医体质自测", layout="centered")
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>中医体质自测问卷</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#555555;'>请根据自己的情况选择分数：1=完全不符合，5=完全符合</h4>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# 用户评分输入
# -------------------------
scores = {}
for constitution, qs in questions.items():
    st.markdown(f"<div style='background-color:#F0F0F0;padding:15px;border-radius:10px;margin-bottom:10px'>"
                f"<h3 style='text-align:center;color:#333333;'>{constitution}</h3></div>", unsafe_allow_html=True)
    scores[constitution] = []
    for q in qs:
        st.markdown(f"<p style='text-align:center;font-size:16px;color:#333;'>{q}</p>", unsafe_allow_html=True)
        score = st.radio("", options=[1, 2, 3, 4, 5], index=2, horizontal=True, key=f"{constitution}_{q}")
        scores[constitution].append(score)

st.markdown("---")

# -------------------------
# 生成 PDF 按钮
# -------------------------
if st.button("生成 PDF 报告"):
    percentages = {c: round(sum(v)/ (5*len(v)) *100,1) for c,v in scores.items()}
    main_constitution = max(percentages, key=percentages.get)

    # 雷达图
    categories = list(percentages.keys())
    values = list(percentages.values())
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2, label="体质百分比", color="#4B8BBE")
    ax.fill(angles, values, alpha=0.25, color="#4B8BBE")
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 100)
    for i,val in enumerate(values[:-1]):
        ax.text(angles[i], val+5, f"{val}%", ha='center', va='bottom', fontsize=9, color='blue')
    ax.set_title("中医体质雷达图", fontsize=14)
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    # PDF
    pdf_buf = BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-50, "中医体质自测报告")

    # 雷达图
    img = ImageReader(buf)
    c.drawImage(img, width/2-150, height-450, width=300, height=300)

    # 主体质描述与建议
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-500, f"主要体质：{main_constitution}")
    c.setFont("Helvetica", 12)
    c.drawString(55, height-520, f"描述：{advice[main_constitution]['description']}")
    c.drawString(55, height-540, f"建议：{advice[main_constitution]['suggestion']}")

    # 各体质百分比
    c.setFont("Helvetica-Bold", 14)
    y = height-570
    c.drawString(50, y, "各体质倾向百分比：")
    y -= 20
    c.setFont("Helvetica", 12)
    for k,v in percentages.items():
        c.drawString(60, y, f"{k}: {v}%")
        y -= 18

    c.showPage()
    c.save()
    pdf_buf.seek(0)

    st.success("PDF 报告生成成功！")
    st.download_button("下载 PDF 报告", pdf_buf, "体质自测报告.pdf", "application/pdf")

    # 页面显示
    st.markdown(f"### 主要体质：{main_constitution}")
    st.markdown(f"**描述**：{advice[main_constitution]['description']}")
    st.markdown(f"**建议**：{advice[main_constitution]['suggestion']}")