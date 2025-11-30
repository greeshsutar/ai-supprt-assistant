import os
from dotenv import load_dotenv
from groq import Groq
from retriever import FAQRetriever

load_dotenv()  # Works locally (.env); on Streamlit we use Secrets

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class SupportAgent:
    def __init__(self):
        self.retriever = FAQRetriever()

    def ask(self, query: str):
        snippets = self.retriever.get_relevant(query)
        context = "\n\n".join(snippets)

        prompt = f"""
You are a support assistant.
Answer ONLY using the context.
If the context does not contain the answer, reply:
"I am not sure. Please contact support."

Context:
{context}

Question:
{query}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # from your list_models.py
            messages=[
                {"role": "system", "content": "You are a helpful support assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return {
            "answer": response.choices[0].message.content,
            "snippets": snippets,
        }
