# agent.py
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from yttools import search_youtube, get_video_stats

agent = create_agent(
    model="anthropic:claude-haiku-4-5-20251001",
    tools=[search_youtube, get_video_stats],
    system_prompt=(
        "You are a YouTube research assistant. "
        "Use search_youtube to find videos, then get_video_stats to look up "
        "how popular specific videos are. Answer the user's question based on "
        "what you find."
    ),
)

if __name__ == "__main__":
    question = "Find some popular Python tutorial videos and tell me which has the most views."
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    for m in result["messages"]:
        m.pretty_print()
