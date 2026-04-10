from httpx import AsyncClient

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings

# Point to Local Llama.cpp server 
llama_cpp_model = OpenAIChatModel(
    "",
    provider = OpenAIProvider(
        # base_url='http://localhost:8080/v1', # Llama Server
        base_url='http://localhost:3000/v1', # Proxy Server for Llama Server
        api_key=''
    ),
    settings = ModelSettings(
        temperature=0.8, 
        max_tokens=160000
    )
)