# app.py
import streamlit as st
from agent import agent   # reuse the agent you already built

st.set_page_config(page_title="YouTube Research Agent", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Research Agent")
st.caption("Ask a research question — the agent searches YouTube, pulls stats, compares videos, then answers.")

TOOL_LABELS = {
    "search_youtube": "🔍 Searching YouTube",
    "get_video_stats": "📊 Fetching video stats",
    "compare_videos": "⚖️ Comparing videos",
}

if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

question = st.chat_input("e.g. Find the 3 most-viewed Python tutorials and what they share")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.history.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        final_answer = ""
        with st.status("Researching…", expanded=True) as status:
            for update in agent.stream(
                {"messages": [{"role": "user", "content": question}]},
                stream_mode="updates",
            ):
                for node_output in update.values():
                    if not isinstance(node_output, dict):
                        continue
                    for msg in node_output.get("messages", []):
                        if getattr(msg, "tool_calls", None):
                            for tc in msg.tool_calls:
                                label = TOOL_LABELS.get(tc["name"], f"🛠️ {tc['name']}")
                                st.write(f"{label} — `{tc['args']}`")
                        elif msg.type == "tool":
                            st.write(f"↳ results from `{msg.name}`")
                        elif msg.type == "ai" and msg.content:
                            final_answer = msg.content
            status.update(label="Done researching", state="complete", expanded=True)

        st.markdown(final_answer or "_(no answer produced)_")

    st.session_state.history.append({"role": "assistant", "content": final_answer})