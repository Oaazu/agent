# agent.py
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from yttools import search_youtube, get_video_stats, compare_videos

agent = create_agent(
    model="anthropic:claude-haiku-4-5-20251001",
    tools=[search_youtube, get_video_stats, compare_videos],
    system_prompt=(
         "You are a YouTube research assistant. "
        "Use search_youtube to find videos, get_video_stats to check a single "
        "video's popularity, and compare_videos to compare several videos side "
        "by side. Plan which tools to use based on the question, then answer "
        "clearly based on what you find.\n\n"
        "When a request asks for videos that are both 'popular' and 'recent', "
        "note that these can be in tension: older videos accumulate more views "
        "simply by being available longer, so the highest view counts usually "
        "belong to older videos. When you encounter this tension, weigh both "
        "factors, consider engagement ratio and publish date alongside raw "
        "views, and briefly explain to the user how you balanced them so your "
        "reasoning is transparent.\n\n"
        "When you mention a specific video in your answer, include its YouTube "
        "URL as a markdown link on the video's title, e.g. "
        "[Video Title](https://www.youtube.com/watch?v=ID), so the user can "
        "click through."
    ),
)

if __name__ == "__main__":
    question = (
        "Find the 3 most-viewed Python tutorial videos and tell me "
         "what they have in common. I care about videos that are both recent "
         "and well-received."
    )
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    for m in result["messages"]:
        m.pretty_print()