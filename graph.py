from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from tools import mock_searxng_search
from typing import TypedDict
from dotenv import load_dotenv
import json

load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


class State(TypedDict, total=False):
    persona: str
    bot_id: str
    topic: str
    context: str
    output: dict



def decide_topic(state: State):
    persona = state.get("persona")

    if not persona:
        raise ValueError(f"Missing persona in state: {state}")

    prompt = f"Based on persona: {persona}, decide a topic."
    topic = model.invoke(prompt).content

    return {
        "persona": persona,
        "bot_id": state["bot_id"],
        "topic": topic
    }



def search(state: State):
    context = mock_searxng_search.invoke(state["topic"])

    return {
        "persona": state["persona"],
        "bot_id": state["bot_id"],
        "topic": state["topic"],
        "context": context
    }




def generate_post(state):
    prompt = f"""
    You are a highly opinionated AI bot.

    Persona: {state['persona']}
    Context: {state['context']}

    Generate a post under 280 characters.

    STRICT RULES:
    - Output ONLY valid JSON
    - No explanation
    - No markdown

    Format:
    {{
        "bot_id": "{state['bot_id']}",
        "topic": "{state['topic']}",
        "post_content": "your post"
    }}
    """

    response = model.invoke(prompt).content.strip()

    try:
        parsed = json.loads(response)
    except:
        
        parsed = {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": response
        }

    return parsed   



def build_graph():
    builder = StateGraph(State)

    builder.add_node("decide", decide_topic)
    builder.add_node("search", search)
    builder.add_node("generate", generate_post)

    builder.set_entry_point("decide")
    builder.add_edge("decide", "search")
    builder.add_edge("search", "generate")

    return builder.compile()