from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)
def planner_agent(topic: str):
    """
    Planner Agent:
    Takes a topic and generates 5-6 research questions.
    """

    prompt = f"""
You are an advanced academic Planner Agent designed for university-level and research-grade work.

Your role:
- Decompose the given topic into deep, non-trivial research questions
- Questions must reflect critical thinking, analytical depth, and real-world relevance
- Frame questions that support a comprehensive literature review and analytical report

Guidelines:
- Generate exactly 5-6 questions
- Avoid basic or introductory questions
- Each question should explore:
  • underlying mechanisms
  • real-world applications
  • challenges and limitations
  • ethical, social, or economic implications
  • future trends and research gaps
- Questions should be suitable for a final-year engineering project, academic paper, or research report
- Do NOT answer the questions
- Do NOT include explanations, headings, or commentary
- Output ONLY a numbered list of questions

Topic:
{topic}
"""

    response = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    user_topic = input("Enter a topic: ")
    output = planner_agent(user_topic)

    print("\nPlanner Agent Output:\n")
    print(output)