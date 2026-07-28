# agent.py
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
# ...rest of your file unchanged
from langchain.agents import create_agent

FAKE_INVENTORY = {"notebooks": 12, "pens": 0, "staplers": 3}

def check_stock(item: str) -> str:
    """Return how many units of a given item are currently in stock.
    
    Args:
        item: The product name to look up,  e.g. "pens"."""

    count = FAKE_INVENTORY.get(item.lower())
    if count is None:
        return f"'{item}' is not a tracked product."
    return f"There are {count} units of {item} in stock."

agent = create_agent(
    model="anthropic:claude-haiku-4-5-20251001",
    tools=[check_stock],
    system_prompt=(
        "You are a helpful inventory assistant.  "
        "Use your tools to answer questions about stock levels."
    ),
)

if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Do we have any pens left in stock?"}]}
    )
    for m in result["messages"]:
        m.pretty_print()