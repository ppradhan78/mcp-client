import os

from dotenv import load_dotenv
from mcp import Client

load_dotenv()


class MCPClientService:

    def __init__(self):
        self.server_url = os.getenv(
            "MCP_SERVER_URL",
            "http://127.0.0.1:8000/mcp"
        )

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict
    ):

        async with Client(self.server_url) as client:

            result = await client.call_tool(
                tool_name,
                arguments
            )

            if result.structured_content is not None:
                return result.structured_content

            return {
                "content": [
                    getattr(item, "text", str(item))
                    for item in result.content
                ]
            }