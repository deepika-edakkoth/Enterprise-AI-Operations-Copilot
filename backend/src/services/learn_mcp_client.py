from langchain_mcp_adapters.client import MultiServerMCPClient

class LearningMCPClient:
    def __init__(self):
        self.mcp_client = None
        self.learn_tools = None

    async def initialize(self):

        self.mcp_client = MultiServerMCPClient(
            {
                "microsoft-learn": {
                    "url": "https://learn.microsoft.com/api/mcp",
                    "transport": "http",
                }
            }
        )

        self.learn_tools = await self.mcp_client.get_tools()

        print(
            "Microsoft Learn MCP tools:",
            [tool.name for tool in self.learn_tools]
        )

    def get_tools(self):
        return self.learn_tools

    def get_client(self):
        return self.mcp_client