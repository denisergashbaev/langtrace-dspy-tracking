import dspy
from langtrace_python_sdk import langtrace
from dotenv import dotenv_values
env_values = dotenv_values()


langtrace.init(api_key=env_values["LANGTRACE_API_KEY"])

lm = dspy.AzureOpenAI(
    model=env_values["AZURE_DEPLOYMENT"],
    max_tokens=4096,
    api_base=env_values["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-02-15-preview",
    api_key=env_values["OPEN_API_KEY"],
    temperature=0,
)