# graph.py

from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from planner import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent


# --------- STATE DEFINITION ----------
class ResearchState(TypedDict):
    topic: str
    questions: List[str]
    research_data: List[Dict]
    report: str


# --------- NODES ----------

def planner_node(state: ResearchState):
    """
    Planner node: generates research questions from topic
    """
    planner_output = planner_agent(state["topic"])

    # Safety check
    if not planner_output:
        return {"questions": []}

    questions = [
        line.split(".", 1)[1].strip()
        for line in planner_output.split("\n")
        if line.strip() and line.strip()[0].isdigit()
    ]

    return {"questions": questions}


def search_node(state: ResearchState):
    """
    Search node: collects research evidence silently
    """
    research_data = []

    for question in state["questions"]:
        result = search_agent(question)
        research_data.append({
            "question": question,
            "results": result.get("results", [])
        })

    return {"research_data": research_data}


def writer_node(state: ResearchState):
    """
    Writer node:
    Generates full academic report in ONE call
    (matches writer_agent.py exactly)
    """

    # 🔥 SPEED OPTIMIZATION: limit research size
    trimmed_data = state["research_data"][:5]

    report = writer_agent(
        state["topic"],
        trimmed_data
    )

    return {"report": report}


# --------- GRAPH ----------

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "search")
    graph.add_edge("search", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
