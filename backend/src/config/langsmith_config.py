import os
from .config import LANGSMITH_API_KEY, LANGSMITH_PROJECT

def configure_langsmith():
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGSMITH_TRACING"] = "true"