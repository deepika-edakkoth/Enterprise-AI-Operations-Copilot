#from src import config
import config.config as config
from langchain_openai import ChatOpenAI

class FoundryModelClient:
    def __init__(self):

        # Initialize LangChain's ChatOpenAI client
        self.model = ChatOpenAI(
            base_url=f"{config.FOUNDRY_ENDPOINT}/openai/v1",
            api_key=config.FOUNDRY_API_KEY,
            model=config.LLM_MODEL_DEPLOYMENT_NAME,
            streaming=True,
            max_completion_tokens=512
        )

    def query(self, prompt: str):
        """Send a prompt to the model and return the response."""
        return self.model.invoke(prompt)
