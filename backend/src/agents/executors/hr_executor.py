from langchain.tools import tool
from langsmith import traceable
from agents.registry import hr_agent

# Wrap it as an async tool so it stays in the async execution path
@tool(description="Use this tool to call the HR Agent for employee policy questions.")
@traceable
async def call_hr_agent(query: str):
    result = await hr_agent.ainvoke({"messages": [{"role": "user", "content": query}]})
    return {
        "status": "success",
        "response": result["messages"][-1].content
    }