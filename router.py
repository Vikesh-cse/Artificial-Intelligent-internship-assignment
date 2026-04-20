from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


personas = {
    "Bot_A": "AI and crypto will solve all problems. Loves Elon Musk and space.",
    "Bot_B": "Tech is destroying society. Hates AI, capitalism, billionaires.",
    "Bot_C": "Focused on markets, ROI, trading, finance."
}


db = FAISS.from_texts(list(personas.values()), embedding)
persona_keys = list(personas.keys())

def route_post_to_bots(post_content: str, threshold: float = 1.5):
    results = db.similarity_search_with_score(post_content, k=3)

    selected = []
    for i, (doc, score) in enumerate(results):
        print(f"Bot: {persona_keys[i]}, Score: {score}")  

        if score <= threshold:
            selected.append(persona_keys[i])

    return selected