import streamlit as st
from planner import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Academic Research Assistant",
    layout="wide"
)

# ---------------- GLOBAL UI STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #fafafa;
}
.header-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 4px;
}
.header-subtitle {
    text-align: center;
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 35px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header-title'>Research Analysis System</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Planner → Search → Writer (Academic Pipeline)</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
topic = st.text_input(
    "Enter Research Topic",
    placeholder="e.g., The Emergence of Agentic AI and Ethical Accountability"
)

generate = st.button("Generate Research Report")

# ---------------- MAIN PIPELINE ----------------
if generate:
    if not topic.strip():
        st.warning("Please enter a valid research topic.")
        st.stop()

    # -------- STEP 1: PLANNER (VISIBLE) --------
    st.subheader("Planner Agent Output")
    planner_output = planner_agent(topic)
    st.markdown(planner_output)

    questions = [
        q.split('.', 1)[1].strip()
        for q in planner_output.split("\n")
        if q.strip() and q[0].isdigit()
    ]

    # -------- STEP 2: SEARCH (HIDDEN) --------
    all_research_data = []
    for question in questions:
        search_results = search_agent(question)
        all_research_data.append({
            "question": question,
            "results": search_results["results"]
        })

    # -------- STEP 3: WRITER --------
    st.subheader("Final Research Report")

    with st.spinner("Synthesizing scholarly literature and generating report..."):
        report = writer_agent(topic, all_research_data)

    # -------- FINAL RENDER (PURE MARKDOWN) --------
    st.markdown(f"# **{topic}**")   # BIG, BOLD TITLE
    st.markdown(report)
