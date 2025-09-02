# The prompt template for the "LLM-as-a-Judge"
# It instructs the judge model to compare two responses and return a structured JSON object.

JUDGE_PROMPT_TEMPLATE = """
You are an impartial and expert AI evaluator. Your task is to analyze two responses from different AI models to a user's prompt and determine which one is better.

[USER PROMPT]:
{prompt}

---

[MODEL A RESPONSE]:
{response_a}

---

[MODEL B RESPONSE]:
{response_b}

---

[EVALUATION INSTRUCTIONS]:
Carefully compare the two responses based on the user's prompt. Consider criteria such as helpfulness, relevance, accuracy, depth, creativity, and clarity.

Your final decision must be in a valid JSON format. Provide a "winner" (must be exactly "model_a" or "model_b") and a concise "reasoning" (a 1-2 sentence explanation for your choice). Do not add any text or formatting outside of the JSON object.

[YOUR VERDICT IN JSON FORMAT]:
"""