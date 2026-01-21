import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock

async def main():
    """Queries Claude Code with a simple prompt and prints the response."""
    async for message in query(prompt="What is 2 + 2? Only provide the final answer in text."):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)



if __name__ == "__main__":
    anyio.run(main)