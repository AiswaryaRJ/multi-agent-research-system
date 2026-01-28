# app.py

import streamlit as st
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from graph import build_graph

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Academic Research Assistant",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>Academic Research Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>Planner → Search → Writer (LangGraph)</p>",
    unsafe_allow_html=True
)

# ---------------- MEMORY SETUP ----------------
MEMORY_FILE = "memory.json"

if "history" not in st.session_state:
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            st.session_state.history = json.load(f)
    except:
        st.session_state.history = []

# ---------------- USER INPUT ----------------
topic = st.text_input(
    "Enter Research Topic",
    placeholder="e.g., Impact of Artificial Intelligence on Education"
)

generate = st.button("Generate Research")

# ---------------- MAIN PIPELINE ----------------
if generate:

    if not topic.strip():
        st.warning("⚠️ Please enter a valid research topic.")
        st.stop()

    initial_state = {
        "topic": topic,
        "questions": [],
        "research_data": [],
        "report": ""
    }

    graph = build_graph()

    planner_container = st.container()
    writer_container = st.container()

    with st.spinner("🤖 Agents are working..."):
        # stream() yields dictionaries like {"node_name": {state_updates}}
        for output in graph.stream(initial_state):
            
            # 1. Handle Planner Output immediately
            if "planner" in output:
                with planner_container:
                    st.markdown("## 🧠 Planner Output (Generated Questions)")
                    questions = output["planner"].get("questions", [])
                    if questions:
                        for q in questions:
                            st.write(f"- {q}")
                    else:
                        st.info("No questions generated.")

            # 2. Handle Writer Output (Final Report)
            if "writer" in output:
                final_report = output["writer"].get("report", "")
                with writer_container:
                    st.markdown("## ✍️ Generated Research Report")
                    st.markdown(final_report)
                    
                    # Store for download button outside loop
                    st.session_state.last_report = final_report

    # If report was generated, show download and save
    if "last_report" in st.session_state and st.session_state.last_report:
        st.download_button(
            label="📄 Download Report (.txt)",
            data=st.session_state.last_report,
            file_name=f"{topic.replace(' ', '_')}.txt",
            mime="text/plain"
        )

        # -------- SAVE TO MEMORY ----------
        entry = {
            "topic": topic,
            "report": st.session_state.last_report,
            "timestamp": str(datetime.now())
        }

        st.session_state.history.append(entry)

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.history, f, indent=2)

# ---------------- PAST REPORTS ----------------
st.markdown("---")
st.markdown("## 🗂️ Past Research Reports")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['topic']} ({item['timestamp']})"):
            st.markdown(item["report"])
            st.download_button(
                label="Download (.txt)",
                data=item["report"],
                file_name=f"{item['topic'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
else:
    st.info("No past research reports yet.")
