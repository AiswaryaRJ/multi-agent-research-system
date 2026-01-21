from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(question: str):
    """
    Search Agent:
    Takes a research question and retrieves relevant web content.
    """

    response = client.search(
        query=question,
        search_depth="advanced",
        max_results=5
    )

    return {
        "question": question,
        "results": response["results"]
    }


if __name__ == "__main__":
    q = input("Enter a research question: ")
    data = search_agent(q)

    print("\nSearch Agent Output:\n")
    for r in data["results"]:
        print(f"- {r['title']}")
        print(f"  {r['content']}\n")
        