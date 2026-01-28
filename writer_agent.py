# writer_agent.py

from openai import OpenAI

# ---------------- CONNECT TO LM STUDIO ----------------
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",  # ✅ FIXED
    api_key="lm-studio"
)

def writer_agent(topic, research_data, section=None, model_name="llama-3.2-3b-instruct"):
    """
    Generates an academic research report for a given topic.
    If section is provided, generates only that section.
    """

    # ---------------- PHASE 1: QUESTION-WISE SUMMARIES ----------------
    summaries = []

    for item in research_data:
        question = item.get("question", "")
        contents = "\n".join(
            r.get("content", "") for r in item.get("results", [])[:4]
        )

        if not contents.strip():
            contents = "No strong evidence found."

        prompt = f"""
You are a research analyst.

Research Question:
{question}

Evidence:
{contents}

Task:
Write a concise academic synthesis (100–150 words).
Focus on consensus, insights, and implications.
Maintain a formal academic tone.
"""

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=900
            )

            if response is None or not response.choices:
                summary = "Summary could not be generated."
            else:
                summary = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️ Writer error for question: {question}")
            print(e)
            summary = "Summary could not be generated due to an error."

        summaries.append((question, summary))

    # ---------------- COMBINE FINDINGS ----------------
    combined_findings = ""
    for i, (q, s) in enumerate(summaries, 1):
        combined_findings += f"\n{i}. {q}\n{s}\n"

    # ---------------- PHASE 2: FINAL REPORT OR SECTION ----------------
    if section:
        final_prompt = f"""
You are an academic research writer.

Research Topic:
{topic}

Section to Write:
{section}

Using the synthesized findings below, write ONLY this section.

Synthesized Findings:
{combined_findings}

Guidelines:
- Stay strictly focused on the given topic and section
- Do not invent unrelated concepts
- Maintain formal academic language
- Ensure logical flow and clarity
"""
    else:
        final_prompt = f"""
You are an academic research writer.

Research Topic:
{topic}

Using the synthesized findings below, write a complete university-level
academic research report.

Required Structure:
- Title
- Abstract
- Introduction
- Thematic Analysis
- Challenges and Limitations
- Ethical and Regulatory Considerations
- Future Scope
- Conclusion

Synthesized Findings:
{combined_findings}

Guidelines:
- Stay strictly focused on the given topic
- Do not invent unrelated concepts
- Maintain formal academic language
- Ensure logical flow and clarity
"""

    try:
        final_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.2,
            max_tokens=3000
        )

        if final_response is None or not final_response.choices:
            return "Final research report could not be generated."

        return final_response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Final report generation failed")
        print(e)
        return "Final research report could not be generated."
