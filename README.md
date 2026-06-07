# Multi-Agent Research System

An autonomous academic research assistant built on a multi-agent architecture. The system decomposes a research topic into structured sub-tasks, retrieves relevant information, and synthesises a final scholarly report — all without manual intervention.

[![Python](https://img.shields.io/badge/Python-3.x-09090b?style=flat-square&logo=python&logoColor=c9a84c)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-09090b?style=flat-square&logo=streamlit&logoColor=c9a84c)](https://streamlit.io)
[![Infosys Springboard](https://img.shields.io/badge/Infosys%20Springboard-Virtual%20Internship-09090b?style=flat-square&logoColor=c9a84c)](https://infosysspringboard.com)

---

## Architecture

```
Planner Agent  →  Search Agent  →  Writer Agent
    │                  │                │
generates           retrieves       synthesises
research plan      evidence         final report
```

Each agent has a single responsibility. State is passed between agents explicitly — no shared globals, no implicit coupling.

| File | Role |
|---|---|
| `planner.py` | Generates university-level research questions from a topic |
| `search_agent.py` | Retrieves and organises supporting evidence per question |
| `writer_agent.py` | Produces academic summaries and a final compiled report |
| `graph.py` | Defines the agent workflow graph and execution order |
| `agents_tools.py` | Shared utility functions available to all agents |
| `app.py` | Streamlit UI — interact with the system via browser |
| `main.py` | CLI entry point |

---

## Getting Started

### Prerequisites

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/)

### Installation

```bash
git clone https://github.com/AiswaryaRJ/multi-agent-research-system.git
cd multi-agent-research-system
pip install -r requirements.txt
```

### Run (CLI)

```bash
python demo_full_pipeline.py
```

### Run (UI)

```bash
streamlit run app.py
```

---

## Tech Stack

`Python` · `Streamlit` · `Multi-Agent Architecture` · `State Management` · `Workflow Graphs`

---

## Background

Built during the **Infosys Springboard Virtual Internship** — first real-world software delivery experience, shipping production-ready code under a defined scope. The focus was on clean agent boundaries, reproducible state, and a modular file structure that scales beyond the internship context.

---

## Author

**Aiswarya Rose Jacob** · [LinkedIn](https://linkedin.com/in/aiswaryarosejacob) · [GitHub](https://github.com/AiswaryaRJ)

`// building with precision · open to opportunities`
