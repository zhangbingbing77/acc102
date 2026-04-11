import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

# ================= 页面配置 =================
st.set_page_config(page_title="中医体质测试", layout="centered")

st.title("🩺 中医体质测试系统")

st.markdown("""
### 📝 评分说明
1 = 从不  
2 = 很少  
3 = 有时  
4 = 经常  
5 = 总是
""")

# ================= 题库（优化版） =================
QUESTIONS = [
    {"q": "你是否容易感到疲劳，即使休息后仍恢复不明显？", "type": "气虚"},
    {"q": "你轻微活动后是否容易气短或不想说话？", "type": "气虚"},

    {"q": "你是否比别人更怕冷，手脚容易发凉？", "type": "阳虚"},
    {"q": "天气变冷时你是否更容易不适或疲倦？", "type": "阳虚"},

    {"q": "你是否经常口干咽燥，即使喝水也不缓解？", "type": "阴虚"},
    {"q": "你是否容易失眠或睡眠浅、多梦？", "type": "阴虚"},

    {"q": "你是否身体困重、精神不清爽？", "type": "痰湿"},
    {"q": "你是否体型偏胖或腹部脂肪较多？", "type": "痰湿"},

    {"q": "你是否面部油脂较多或容易长痘？", "type": "湿热"},
    {"q": "你是否有口苦或大便黏滞不爽？", "type": "湿热"},

    {"q": "你是否有固定部位针刺样疼痛或不适？", "type": "血瘀"},
    {"q": "你是否面色偏暗或容易有瘀斑？", "type": "血瘀"},

    {"q": "你是否经常情绪低落或容易叹气？", "type": "气郁"},
    {"q": "你在压力下是否容易焦虑或难以放松？", "type": "气郁"},

    {"q": "你是否容易过敏（鼻炎、皮肤过敏等）？", "type": "特禀"},
    {"q": "你是否对气味、花粉或食物较敏感？", "type": "特禀"},

    {"q": "你是否精力充沛，很少疲劳？", "type": "平和"},
    {"q": "你是否睡眠良好、饮食正常？", "type": "平和"},
    {"q": "你是否情绪稳定、适应能力强？", "type": "平和"},
    {"q": "你是否很少生病，整体状态良好？", "type": "平和"},
]

# ================= 体质说明库 =================
CONSTITUTION_INFO = {
    "气虚": {
        "desc": "气虚质：元气不足，容易疲劳、气短、懒言。",
        "advice": [
            "避免过度劳累",
            "保证充足睡眠",
            "多吃山药、红枣、黄芪等"
        ]
    },
    "阳虚": {
        "desc": "阳虚质：阳气不足，怕冷、四肢不温。",
        "advice": [
            "注意保暖",
            "少吃生冷食物",
            "可适当食用羊肉、生姜"
        ]
    },
    "阴虚": {
        "desc": "阴虚质：体内津液不足，口干、失眠。",
        "advice": [
            "避免熬夜",
            "少辛辣食物",
            "多吃百合、银耳"
        ]
    },
    "痰湿": {
        "desc": "痰湿质：代谢偏慢，身体困重、易胖。",
        "advice": [
            "控制饮食油腻",
            "加强运动",
            "保持规律作息"
        ]
    },
    "湿热": {
        "desc": "湿热质：内热湿重，易长痘、口苦。",
        "advice": [
            "避免辛辣油炸",
            "清淡饮食",
            "注意肠胃调理"
        ]
    },
    "血瘀": {
        "desc": "血瘀质：血液循环不畅，易刺痛、肤色暗。",
        "advice": [
            "适当运动",
            "避免久坐",
            "多吃山楂"
        ]
    },
    "气郁": {
        "desc": "气郁质：情绪不畅，易压抑、焦虑。",
        "advice": [
            "保持心情舒畅",
            "多运动",
            "多社交"
        ]
    },
    "特禀": {
        "desc": "特禀质：过敏体质，鼻炎或皮肤敏感。",
        "advice": [
            "避免过敏源",
            "增强免疫力",
            "保持环境清洁"
        ]
    },
    "平和": {
        "desc": "平和质：身体健康，阴阳平衡。",
        "advice": [
            "保持良好作息",
            "均衡饮食",
            "适量运动"
        ]
    }
}

# ================= 答题 =================
options = {"从不": 1, "很少": 2, "有时": 3, "经常": 4, "总是": 5}

answers = []

for i, item in enumerate(QUESTIONS, 1):
    st.markdown(f"### {i}. {item['q']}")

    choice = st.radio("", list(options.keys()), horizontal=True, key=i)
    answers.append((item["type"], options[choice]))

    st.divider()

# ================= 计算 =================
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
        result[t] = round((raw[t] - min_s) / (max_s - min_s) * 100, 2)

    return result

# ================= 雷达图 =================
def draw_chart(result):
    labels = list(result.keys())
    values = list(result.values())

    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(angles[:-1]*180/np.pi, labels)
    ax.set_title("中医体质雷达图")

    return fig

# ================= 保存 =================
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

# ================= 结果页面 =================
if st.button("🚀 生成体质报告"):

    result = calculate(answers)

    # ===== 主体质 =====
    main_type, main_score = max(result.items(), key=lambda x: x[1])

    st.subheader("🏥 你的体质类型")
    st.success(f"{main_type}（{main_score}%）")

    # ===== 说明 =====
    info = CONSTITUTION_INFO.get(main_type)

    st.subheader("📖 体质说明")
    st.write(info["desc"])

    st.subheader("⚠️ 调理建议")
    for item in info["advice"]:
        st.write("• " + item)

    # ===== 雷达图 =====
    st.subheader("📊 体质分布")
    fig = draw_chart(result)
    st.pyplot(fig)

    # ===== 其他体质 =====
    st.subheader("📌 其他体质参考")
    for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{k}: {v}%")

    # ===== 保存 =====
    save(result)

    st.success("已保存到历史记录")