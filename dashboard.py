
import json
from pathlib import Path
from collections import Counter

import streamlit as st
import pandas as pd

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BeeStudy Analytics",
    page_icon="🐝",
    layout="wide"
)

# Find the project folder automatically
BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "data" / "results" / "study_results.json"

# ============================================================
# 2. LOAD SAVED RESULTS
# ============================================================

def load_results():
    try:
        with open(RESULT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]

        return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ============================================================
# 3. DASHBOARD HEADER
# ============================================================

st.title("🐝 BeeStudy")
st.subheader("Study Progress & Learning Analytics")

st.write(
    "Track your study sessions, quiz scores and revision topics."
)

st.caption(
    "Prototype dashboard | Current study records are locally saved "
    "and may contain simulated data."
)

results = load_results()

# ============================================================
# 4. EMPTY STATE
# ============================================================

if not results:
    st.info(
        "No study results found. Run `python main.py` "
        "and complete the quiz to get started."
    )
    st.stop()

# ============================================================
# 5. PREPARE ANALYTICS
# ============================================================

records = []

for number, result in enumerate(results, start=1):
    try:
        percentage = float(result.get("percentage", 0) or 0)
        duration = float(result.get("duration_minutes", 0) or 0)
        score = int(result.get("score", 0) or 0)
        total = int(result.get("total_questions", 0) or 0)
    except (ValueError, TypeError):
        continue

    records.append({
        "Session": f"Session {number}",
        "Percentage": percentage,
        "Study Minutes": duration,
        "Score": score,
        "Total Questions": total,
        "Subject": str(result.get("subject", "Not specified")),
        "Student": str(result.get("student", "Student")),
        "Activity": str(result.get("activity", "Study")),
        "Topics": result.get("topics_detected", [])
    })

if not records:
    st.warning("Saved results could not be processed.")
    st.stop()

df = pd.DataFrame(records)

# ============================================================
# 6. TOP SUMMARY CARDS
# ============================================================

st.markdown("## 📊 Your Progress")

total_sessions = len(df)
total_minutes = df["Study Minutes"].sum()
average_score = df["Percentage"].mean()
latest_score = df.iloc[-1]["Percentage"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Study Sessions", total_sessions)
col2.metric("Total Study Time", f"{total_minutes:g} min")
col3.metric("Average Score", f"{average_score:.1f}%")
col4.metric("Latest Score", f"{latest_score:.1f}%")

# ============================================================
# 7. QUIZ SCORE PROGRESS CHART
# ============================================================

st.markdown("---")
st.markdown("## 📈 Quiz Performance")

st.write("Compare your quiz percentage across study sessions.")

score_chart = df[["Session", "Percentage"]].set_index("Session")

st.line_chart(score_chart, y="Percentage")

# ============================================================
# 8. STUDY TIME CHART
# ============================================================

st.markdown("## ⏱️ Study Time")

st.write("See how much time you spent in each session.")

time_chart = df[["Session", "Study Minutes"]].set_index("Session")

st.bar_chart(time_chart, y="Study Minutes")

# ============================================================
# 9. TOPIC ANALYSIS
# ============================================================

st.markdown("---")
st.markdown("## 📚 Topics Practised")

topic_counts = Counter()

for topics in df["Topics"]:
    if isinstance(topics, list):
        for topic in topics:
            topic_counts[str(topic)] += 1

if topic_counts:
    topic_df = pd.DataFrame(
        topic_counts.items(),
        columns=["Topic", "Sessions"]
    ).set_index("Topic")

    st.bar_chart(topic_df, y="Sessions")

    st.write("Topics detected in your saved sessions:")

    for topic, count in topic_counts.most_common():
        st.write(f"✅ **{topic}** — detected in {count} session(s)")

else:
    st.info("No detected topics are available yet.")

# ============================================================
# 10. STUDY HISTORY
# ============================================================

st.markdown("---")
st.markdown("## 🗂️ Study History")

for record in reversed(records):
    with st.expander(record["Session"]):
        st.write("**Student:**", record["Student"])
        st.write("**Subject:**", record["Subject"])
        st.write("**Activity:**", record["Activity"])
        st.write("**Study Time:**", f'{record["Study Minutes"]:g} minutes')
        st.write(
            "**Quiz Score:**",
            f'{record["Score"]} / {record["Total Questions"]}'
        )
        st.write("**Percentage:**", f'{record["Percentage"]:.1f}%')

        topics = record["Topics"]

        if isinstance(topics, list) and topics:
            st.write("**Topics:**", ", ".join(map(str, topics)))
        else:
            st.write("**Topics:** No topics recorded")

# ============================================================
# 11. REFRESH DASHBOARD
# ============================================================

st.markdown("---")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

st.caption(
    "🐝 BeeStudy prototype | Keep simulated data separate "
    "from any future real wearable-device data."
)
# ============================================================
# BEESTUDY INTERACTIVE QUIZ
# ============================================================

import streamlit as st

st.markdown("---")
st.header("🐝 BeeStudy Interactive Quiz")

quiz_questions = [
    {
        "question": "What is a differential amplifier?",
        "options": [
            "An amplifier that amplifies the difference between two inputs",
            "An amplifier that amplifies only DC",
            "A circuit that stores energy",
            "An amplifier that produces no output"
        ],
        "answer": "An amplifier that amplifies the difference between two inputs"
    },
    {
        "question": "What is differential gain?",
        "options": [
            "Output voltage divided by differential input voltage",
            "Input current divided by resistance",
            "Common-mode output divided by supply voltage",
            "Resistance divided by capacitance"
        ],
        "answer": "Output voltage divided by differential input voltage"
    },
    {
        "question": "What does CMRR stand for?",
        "options": [
            "Common Mode Rejection Ratio",
            "Current Mode Resistance Ratio",
            "Common Maximum Response Range",
            "Collector Mode Resistance Ratio"
        ],
        "answer": "Common Mode Rejection Ratio"
    },
    {
        "question": "For a good differential amplifier, common-mode gain should be:",
        "options": [
            "As low as possible",
            "As high as possible",
            "Equal to the supply voltage",
            "Always infinite"
        ],
        "answer": "As low as possible"
    }
]

with st.form("beestudy_quiz"):
    selected_answers = {}

    for i, item in enumerate(quiz_questions):
        selected_answers[i] = st.radio(
            f"Question {i + 1}: {item['question']}",
            item["options"],
            index=None,
            key=f"quiz_question_{i}"
        )

    submitted = st.form_submit_button("Submit Quiz")

if submitted:
    score = 0

    for i, item in enumerate(quiz_questions):
        if selected_answers[i] == item["answer"]:
            score += 1
            st.success(f"Question {i + 1}: Correct!")
        else:
            st.error(f"Question {i + 1}: Incorrect.")
            st.write("Correct answer:", item["answer"])

    percentage = (score / len(quiz_questions)) * 100

    st.subheader("🏆 Your Quiz Result")
    st.write(f"**Score:** {score}/{len(quiz_questions)}")
    st.progress(int(percentage))
    st.write(f"**Percentage:** {percentage:.1f}%")

    if percentage >= 75:
        st.balloons()
        st.success("Excellent work! 🎉")
    elif percentage >= 50:
        st.info("Good attempt! Revise the topics once.")
    else:
        st.warning("Keep practising, macha! 💪")