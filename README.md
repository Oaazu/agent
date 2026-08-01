# 🎬 YouTube Research Agent

An agentic LLM that plans, calls tools in a loop, and synthesizes an answer — built with LangChain 1.x and the YouTube Data API v3.

**🔗 [Live demo](https://deployagent.streamlit.app)** · Ask it something like *"Find the 3 most-viewed machine learning tutorials and tell me what they have in common."*

---

## What makes it an *agent*

Most LLM apps run a fixed pipeline: the developer hardcodes the steps, and the model fills in the blanks. This project is different — the LLM decides what to do.

Given a research question, the agent plans which tools to call, calls them in a loop, reads each result, and decides its next move — until it has enough to answer. Nothing about the sequence is hardcoded.

User question
↓
[Agent plans] → search_youtube → reads results
↓
[Agent plans] → get_video_stats (×N, in parallel) → reads stats
↓
[Agent plans] → compare_videos → reads comparison
↓
[Agent synthesizes final answer]

This is the LangChain 1.x `create_agent` reasoning loop: the model is called, and if it requests a tool, the tool runs and its result is fed back, and the model is called again — repeating until it produces a final answer.

## The three tools

Each tool is a plain Python function the agent chooses between at runtime, based on its docstring:

| Tool | Purpose |
|------|---------|
| `search_youtube(query)` | Finds candidate videos for a topic and returns their titles, channels, IDs, and URLs. |
| `get_video_stats(video_id)` | Looks up views, likes, and publish date for one video. |
| `compare_videos(video_ids)` | Compares several videos side by side, computing a like-to-view engagement ratio. |

The tools have a natural dependency: `get_video_stats` needs a `video_id` that only `search_youtube` can produce. This forces the agent to chain them in sequence — search first, then stats — which is the core "plan across steps" behavior.

## Tech stack

- **LangChain 1.x** — `create_agent`, the current standard that replaced the older `AgentExecutor` pattern (deprecated in LangChain 1.0)
- **Anthropic Claude** — the reasoning model driving the agent
- **YouTube Data API v3** — live video data
- **Streamlit** — a chat UI that streams the agent's tool calls live, so you can watch it reason
- **Streamlit Community Cloud** — deployment

## Running it locally

```bash
# clone and enter the project
git clone https://github.com/Oaazu/agent.git
cd agent

# create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate          # macOS/Linux

# install dependencies
pip install -r requirements.txt

# add your API keys (see .env.example)
# create a .env file containing:
#   ANTHROPIC_API_KEY=your-key
#   YOUTUBE_API_KEY=your-key

# run the app
streamlit run app.py
```

## Project structure

yttools.py # the three tools (search, stats, compare)
agent.py # the agent definition and system prompt
app.py # the Streamlit chat UI
.streamlit/config.toml # theme
.env.example # template for required API keys
requirements.txt # dependencies
The split is deliberate: tools, agent logic, and UI each live in their own file with one job.

## Things I learned building this

- **Tool descriptions are prompt engineering.** The agent picks tools based entirely on their docstrings — vague wording produces wrong or skipped tool calls.
- **Parallel vs. sequential tool calls.** Independent calls (looking up stats for five videos) run in parallel; dependent ones (search → stats) must run in sequence. I hit a real thread-safety bug when parallel calls shared a single API client, and fixed it by giving each call its own client.
- **Prompting shapes behavior probabilistically, not deterministically.** Tuning the system prompt to handle the "most-viewed vs. recent" tension made the agent *explain* the tradeoff reliably, but act on it less consistently — a lesson in when to reach for code instead of prompts.
- **"Works on my machine" ≠ "works in production."** The deployed environment used a newer Python version and had a flaky API discovery fetch that never appeared locally; fixed with static discovery.

## Scope

Deliberately minimal: one agent, three tools, one loop, deployed. No multi-agent orchestration, memory, or persistence — a focused project that works beats an ambitious one that's half-built.
