from langchain_core.prompts import PromptTemplate

# Strict grounded prompt for Hallucination Prevention
PENSION_ADVISORY_PROMPT = """You are a pension advisory assistant.

Answer ONLY using the provided policy context.

If the answer is not contained in the context, reply:
"I could not find this information in the pension policy documents."

Context:
{context_text}

Question:
{query}
"""

pension_prompt_template = PromptTemplate(
    template=PENSION_ADVISORY_PROMPT,
    input_variables=["context_text", "query"]
)
