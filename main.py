import streamlit as st
import json
import random

# --- Load quiz data from JSON file ---
with open("quiz_data.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

# --- Session State Initialization ---
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.filtered_data = []

# --- Step 1: Collect User Info ---
if st.session_state.user_info is None:
    st.title("📘 Prompt Engineering Mastery Quiz App")

    name = st.text_input("✍️ Enter your name:")
    level = st.selectbox(
        "🎯 Select your level:", ["Beginner", "Intermediate", "Advanced"]
    )

    # ✅ Fix: filter data for selected level first
    level_data = [q for q in quiz_data if q.get("level") == level]
    available_count = len(level_data)

    # Agar selected level me koi question na ho, fallback
    if available_count == 0:
        st.warning(f"No questions found for {level} level.")
        st.stop()

    question_limit = st.selectbox(
        "📌 How many questions do you want to attempt?",
        options=["All"] + list(range(1, available_count + 1)),
    )

    if st.button("🚀 Start Quiz", use_container_width=True):
        if name.strip() == "":
            st.warning("⚠️ Please enter your name to continue.")
        else:
            st.session_state.user_info = {"name": name, "level": level}

            # Apply question limit correctly
            if question_limit == "All":
                st.session_state.filtered_data = level_data
            else:
                st.session_state.filtered_data = random.sample(
                    level_data, int(question_limit)
                )

            st.rerun()

# --- Step 2: Quiz Questions ---
elif st.session_state.q_index < len(st.session_state.filtered_data):
    q = st.session_state.filtered_data[st.session_state.q_index]

    st.markdown(f"### 🎯 Level: **{st.session_state.user_info['level']}**")
    st.markdown("---")

    # Progress bar
    progress = (st.session_state.q_index) / len(st.session_state.filtered_data)
    st.progress(progress)
    st.write(
        f"**Progress:** {st.session_state.q_index}/{len(st.session_state.filtered_data)}"
    )

    # Question card
    with st.container():
        st.subheader(f"Q{st.session_state.q_index + 1}: {q['question']}")
        st.caption(f"📌 Topic: {q.get('topic', 'General')}")

        user_answer = st.radio(
            "👉 Choose one:", q["options"], key=f"q{st.session_state.q_index}"
        )

    # Next button
    if st.button("➡️ Next", use_container_width=True):
        st.session_state.answers.append(
            {
                "question": q["question"],
                "user_answer": user_answer,
                "correct_answer": q["correct_answer"],
                "level": q.get("level", "N/A"),
                "topic": q.get("topic", "General"),
            }
        )

        if user_answer == q["correct_answer"]:
            st.session_state.score += 1

        st.session_state.q_index += 1
        st.rerun()

# --- Step 3: Results ---
else:
    st.success(f"🎉 Hi {st.session_state.user_info['name']} 👋")
    st.write(f"📊 Level: {st.session_state.user_info['level']}")
    st.success(
        f"✅ Your Score: {st.session_state.score} / {len(st.session_state.filtered_data)}"
    )

    if st.session_state.score == len(st.session_state.filtered_data):
        st.info("🏆 Excellent! You nailed it.")
    elif st.session_state.score >= len(st.session_state.filtered_data) // 2:
        st.info("👍 Good job! Keep practicing to improve further.")
    else:
        st.info("📖 Needs improvement. Review the concepts and try again.")

    st.subheader("📝 Review Your Answers:")
    for i, ans in enumerate(st.session_state.answers):
        st.markdown(f"**Q{i + 1}: {ans['question']}**")
        st.write(f"- ✍️ Your Answer: {ans['user_answer']}")
        st.write(f"- ✅ Correct Answer: {ans['correct_answer']}")
        st.write(f"- 📌 Topic: {ans['topic']} | Level: {ans['level']}")
        if ans["user_answer"] == ans["correct_answer"]:
            st.success("✅ Correct")
        else:
            st.error("❌ Wrong")

    if st.button("🔄 Restart Quiz", use_container_width=True):
        st.session_state.user_info = None
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.filtered_data = []
        st.rerun()

# --- Download Resources ---
with open("resources/prompt engieering guide.pdf", "rb") as f:
    pdf_data = f.read()

with open(
    "resources/Complete_Prompt_Engineering_Master_Guide - Basics to Advanced.pdf",
    "rb",
) as f:
    pdf_data_roman = f.read()


st.download_button(
    label="📥 Download Google official prompt engineering guide",
    data=pdf_data,
    file_name="google_prompt_engineering.pdf",
    mime="application/pdf",
)
st.download_button(
    label="📥 Download My prompt Engineering Complete guide Notes in Roman Urdu",
    data=pdf_data_roman,
    file_name="huzaifa_roman_urdu_prompt_engineering.pdf",
    mime="application/pdf",
)


# --- Footer ---
st.markdown("---")
st.markdown(
    "Connect with me: **[Personal Portfolio](https://huzaifa-mukhtar-official.vercel.app/)**"
)
st.markdown("Connect with me: **[Github](https://github.com/Huzaifa4412)**")
st.markdown(
    "Connect with me: **[Linkedin](https://www.linkedin.com/in/huzaifa-mukhtar-8ba0492b5/)**"
)

st.markdown("Made with ❤️ by **Huzaifa Mukhtar**")
