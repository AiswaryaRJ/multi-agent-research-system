from openai import OpenAI

# ✅ Correct LM Studio connection
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def planner_agent(topic: str):
    """
    Planner Agent:
    Generates 5–6 deep research questions.
    """

    prompt = f"""
You are an advanced academic Planner Agent designed for university-level and research-grade work.

Your role:
- Decompose the given topic into deep, non-trivial research questions

Guidelines:
- Generate exactly 5–6 questions
- Avoid basic or introductory questions
- Do NOT answer the questions
- Output ONLY a numbered list

Topic:
{topic}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",  # MUST match LM Studio
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=400
        )

        # ✅ SAFETY CHECK
        if response is None or not response.choices:
            return ""

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Planner agent failed")
        print(e)
        return ""
