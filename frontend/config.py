import os

#Langsmith API Key
LANGSMITH_API_KEY = "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"
LANGSMITH_PROJECT = "enterprise-ai-copilot"
API_BASE_URL = "http://localhost:8000/"

def configure_langsmith():
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGSMITH_TRACING"] = "true"