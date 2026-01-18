# demo_planner_search.py

from planner import planner_agent
from search_agent import search_agent

def run_demo():
    print("\n==================== OPEN DEEP RESEARCHER DEMO ====================\n")

    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("Please enter a valid topic.")
        return

    # STEP 1: Planner Agent
    print(f"\n[STEP 1] Planner Agent: Generating research questions for topic: '{topic}'...\n")
    questions_text = planner_agent(topic)

    questions = [
        q.strip().split('.', 1)[1].strip()
        for q in questions_text.split("\n")
        if q.strip() and q[0].isdigit()
    ]

    print(f"✅ Generated {len(questions)} research questions:\n")
    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q}")

    # STEP 2: Search Agent
    print("\n[STEP 2] Search Agent: Retrieving web content for ALL questions...\n")

    all_research_data = []

    for idx, question in enumerate(questions, start=1):
        print(f"\n🔹 Question {idx}: {question}\n")

        results = search_agent(question)

        print(f"Retrieved {len(results.get('results', []))} results\n")

        all_research_data.append({
            "question": question,
            "results": results.get("results", [])
        })

        for r_idx, r in enumerate(results.get("results", []), start=1):
            snippet = r.get("content", "No content")[:200].replace("\n", " ")
            print(f" {r_idx}. {r.get('title', 'No Title')}: {snippet}...\n")

    print("\n✅ Planner + Search pipeline completed successfully.")
    print("➡ All questions have been answered by the Search Agent.")
    print("➡ Data is ready for Writer Agent synthesis.\n")
    print("====================================================================\n")

    return all_research_data


if __name__ == "__main__":
    run_demo()

