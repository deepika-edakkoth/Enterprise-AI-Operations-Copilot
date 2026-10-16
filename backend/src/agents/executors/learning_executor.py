from langchain.tools import tool
from langsmith import traceable
from agents import registry

# Wrap it as an async tool so it stays in the async execution path
@tool(description="Use this tool to call the Learning Agent for Azure and Microsoft technologies.")
@traceable
async def call_learn_agent(query: str):
    print (f"Calling Learning Agent with query: {query}")
    result = await registry.learning_agent.ainvoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content