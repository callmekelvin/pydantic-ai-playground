from pydantic_ai import Embedder
from pydantic_ai.embeddings.openai import OpenAIEmbeddingModel
from pydantic_ai.providers.openai import OpenAIProvider

# Point to Local Llama.cpp server for Embedding Model
llama_cpp_embedding_model = OpenAIEmbeddingModel(
    "qwen3-embedding-4b",
    provider = OpenAIProvider(
        base_url='http://localhost:9090/v1', # Llama Server for Embedding Model
        api_key=''
    )
)

embedder = Embedder(llama_cpp_embedding_model)