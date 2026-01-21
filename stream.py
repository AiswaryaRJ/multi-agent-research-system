import streamlit as st
from planner import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Research Analysis System",
    layout="wide"
)

st.title("Research Analysis System")
st.caption("Multi-Agent Research Pipeline (Planner → Search → Writer)")

# ---------------- INPUT ----------------
topic = st.text_input("Enter research topic")

# ---------------- REPORT STYLING ----------------
st.markdown("""
<style>
.research-container {
    font-family: Georgia, serif;
    line-height: 1.8;
    font-size: 17px;
}
.research-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 30px;
}
.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- BUTTON ACTION ----------------
if st.button("Generate Research Report"):
    if not topic.strip():
        st.warning("Please enter a valid research topic.")
        st.stop()

    # -------- STEP 1: PLANNER (VISIBLE) --------
    st.subheader("Planner Agent Output")
    planner_output = planner_agent(topic)
    st.write(planner_output)

    # Extract questions
    questions = [
        q.split('.', 1)[1].strip()
        for q in planner_output.split("\n")
        if q.strip() and q[0].isdigit()
    ]

    # -------- STEP 2: SEARCH (HIDDEN) --------
    all_research_data = []
    with st.spinner("Retrieving and analyzing scholarly sources..."):
        for question in questions:
            search_results = search_agent(question)
            all_research_data.append({
                "question": question,
                "results": search_results["results"]
            })

    # -------- STEP 3: WRITER (VISIBLE FINAL OUTPUT) --------
    st.subheader("Final Research Report")
    with st.spinner("Synthesizing research into academic report..."):
        report = writer_agent(topic, all_research_data)

    # -------- RENDER FINAL REPORT --------
    st.markdown(f"""
    <div class="research-container">
        <div class="research-title">{topic}</div>

        <div class="section-title">Abstract</div>
        <p>{report[:600]}...</p>

        <div class="section-title">Introduction</div>
        <p>{report}</p>

        <div class="section-title">Discussion</div>
        <p>
        This section synthesizes findings across multiple scholarly sources,
        identifying conceptual patterns, theoretical implications, and
        emerging research directions.
        </p>

        <div class="section-title">Limitations</div>
        <p>
        The analysis is limited by source availability, potential publication bias,
        and the rapidly evolving nature of the research domain.
        </p>

        <div class="section-title">Conclusion</div>
        <p>
        The study demonstrates the academic relevance of the topic and provides
        a strong foundation for future research and real-world application.
        </p>
    </div>
    """, unsafe_allow_html=True)
