from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

# HTTP Client making requests to Llama.cpp
http_client = AsyncClient(timeout=3600)

# Point to Local Llama.cpp server 
model = OpenAIChatModel(
    "",
    provider = OpenAIProvider(
        base_url='http://localhost:8080/v1',
        api_key='',
        # http_client=http_client
    ),
    settings = ModelSettings(
        temperature=0.8, 
        max_tokens=160000
    )
)

agent = Agent(model)

result = agent.run_sync('How to resolve heap issue?')  
print(result.output)