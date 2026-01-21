from planner import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent


def run_demo():
    print("\n==================== MULTI-AGENT RESEARCH SYSTEM ====================\n")

    topic = input("Enter research topic: ").strip()
    if not topic:
        print("Invalid topic")
        return

    # STEP 1: PLANNER AGENT
    print("\n[STEP 1] Planner Agent Output:\n")
    planner_output = planner_agent(topic)

    questions = [
        q.split('.', 1)[1].strip()
        for q in planner_output.split("\n")
        if q.strip() and q[0].isdigit()
    ]

    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q}")

    # STEP 2: SEARCH AGENT
    print("\n[STEP 2] Search Agent Output (Question + Retrieved Content):\n")

    all_research_data = []

    for idx, question in enumerate(questions, start=1):
        print(f"\n🔹 Research Question {idx}:")
        print(question)

        search_results = search_agent(question)

        print("\nRetrieved Content:")
        for r_idx, r in enumerate(search_results["results"], start=1):
            snippet = r["content"][:300].replace("\n", " ")
            print(f"{r_idx}. {snippet}...\n")

        all_research_data.append({
            "question": question,
            "results": search_results["results"]
        })

    # STEP 3: WRITER AGENT
    print("\n[STEP 3] Writer Agent: Final Research Report\n")

    report = writer_agent(topic, all_research_data)

    print("\n==================== FINAL RESEARCH REPORT ====================\n")
    print(report)
    print("\n================================================================\n")


if __name__ == "__main__":
    run_demo()
