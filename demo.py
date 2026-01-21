from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def writer_agent(topic: str, research_data: list):
    """
    Writer Agent:
    Generates a detailed, professional, university-level research report
    strictly based on retrieved search content.
    """

    compiled_content = ""

    for idx, item in enumerate(research_data, start=1):
        compiled_content += f"\nResearch Question {idx}: {item['question']}\n"
        for r in item["results"]:
            compiled_content += f"{r['content']}\n"

    prompt = f"""
You are a senior academic Writer Agent producing a FINAL research report.

CRITICAL REQUIREMENTS (DO NOT VIOLATE):
- Use ONLY the retrieved content provided
- Do NOT invent new facts
- Maintain formal academic tone
- Write in full paragraphs (no bullet points)
- Each section MUST contain multiple paragraphs
- Each section MUST be at least 120–180 words
- Ensure depth, explanation, and synthesis

MANDATORY REPORT STRUCTURE AND DEPTH:

Title

Abstract (150–200 words)

1. Introduction
   - Minimum 2 detailed paragraphs
   - Explain background, motivation, and significance

2. Literature Review and Thematic Analysis
   - Minimum 3 detailed paragraphs
   - Compare and synthesize ideas across ALL research questions

3. Practical Applications and Methodologies
   - Minimum 2 detailed paragraphs
   - Explain how concepts are applied in real-world scenarios

4. Challenges and Limitations
   - Minimum 2 detailed paragraphs
   - Discuss technical, ethical, and operational challenges

5. Ethical, Social, and Economic Implications
   - Minimum 2 detailed paragraphs
   - Analyze broader societal impact

6. Future Scope and Research Directions
   - Minimum 2 detailed paragraphs
   - Discuss future trends and open problems

7. Conclusion
   - Minimum 1–2 detailed paragraphs
   - Summarize contributions and findings

RESEARCH TOPIC:
{topic}

RETRIEVED CONTENT (USE THIS ONLY):
{compiled_content}
"""

    response = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2500
    )

    return response.choices[0].message.content
