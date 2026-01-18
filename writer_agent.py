# writer_agent.py

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def writer_agent(topic, research_data):
    """
    research_data = [
        {
            "question": "...",
            "results": [
                {"content": "..."},
                {"content": "..."}
            ]
        }
    ]
    """

    question_summaries = []

    # -------- PHASE 1: QUESTION-WISE SUMMARIZATION --------
    for item in research_data:
        question = item["question"]

        # ✅ FIX: extract content correctly
        contents = "\n".join(
            r["content"] for r in item.get("results", [])[:3]
        )

        prompt = f"""
You are a research analyst.

Research Question:
{question}

Retrieved Evidence:
{contents}

Task:
Write a concise academic summary (120–150 words).
Focus on key findings, consensus, and implications.
Maintain formal tone.
"""

        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        summary = response.choices[0].message.content
        question_summaries.append((question, summary))

    # -------- PHASE 2: FINAL RESEARCH REPORT --------
    combined_findings = ""
    for i, (q, s) in enumerate(question_summaries, 1):
        combined_findings += f"\n{i}. {q}\n{s}\n"

    final_prompt = f"""
You are an academic research writer.

Topic:
{topic}

Write a professional university-level research report using the analyzed findings below.

Structure:
- Title
- Abstract
- Introduction
- Thematic Analysis
- Challenges and Limitations
- Ethical and Regulatory Considerations
- Future Scope
- Conclusion

Findings:
{combined_findings}

Style:
Formal, precise, analytical, and well-structured.
"""

    final_response = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.2
    )

    return final_response.choices[0].message.content
