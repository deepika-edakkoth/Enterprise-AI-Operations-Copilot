from langchain_core.tools import tool
from random import randint

@tool
def get_knowledge(location: str) -> str:
    """Get the current weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    temp = randint(10, 30)
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {temp}°C."