import json
from langchain_core.messages import ToolMessage

async def extract_approval(response):

    for msg in response["messages"]:
        if isinstance(msg, ToolMessage):

            try:
                data = json.loads(msg.content)

                if data.get("status") == "pending_approval":
                    return data["interrupt"]

            except Exception:
                continue

    return None