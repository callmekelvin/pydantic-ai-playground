from pydantic_ai import Agent, RunContext, Tool

from llamaCppGenerativeModel import llama_cpp_generative_model
from llamaCppEmbeddingModel import embedder
from redisManager import RedisManager

import asyncio
import numpy as np
import os

instructions = """
You are a CLI Agent specialized in answering questions about the Godot Game Engine.

Your purpose is to help users understand, debug, and build projects using Godot by providing accurate, concise, and practical answers based on official documentation.

You have access to a tool called `godot_game`, which retrieves information from a RAG store built on the official Godot Engine documentation. You MUST use this tool when:
- The question involves specific Godot features, APIs, nodes, functions, or workflows
- You are unsure of exact details or syntax
- The user asks for documentation-based explanations or examples

Guidelines:
- Prefer information from the `godot_game` tool over prior knowledge when available
- Provide clear, CLI-style responses: concise, structured, and actionable
- Include code snippets when helpful
- If the tool does not return useful results, fall back to general knowledge and clearly state that
- Do not hallucinate APIs, functions, or behavior—only provide verified information
- Keep responses focused strictly on Godot unless the user explicitly asks otherwise

Output Style:
- Be direct and minimal
- Use bullet points or short sections when appropriate
- Avoid unnecessary explanation unless requested

You are not a general assistant—you are a focused Godot CLI expert.
"""

cliAgent = Agent(
    model=llama_cpp_generative_model,
    instructions=instructions,
    output_type=str
)

@cliAgent.tool
async def godot_game_docs(ctx: RunContext[str]) -> list[str]:
    print("Godot Game Docs Tool Triggered")

    redis = RedisManager()
    await redis.createRedisConnection()

    # Embed User Prompt
    user_prompt = ctx.prompt.lower()
    embedPromptResult = await embedder.embed_query(user_prompt)
    # print(embedPromptResult)

    # Query User Prompt Embed with Redis VL
    redisQueryResult = await redis.query(
        vector = np.array(embedPromptResult.embeddings[0]),
        noResults = 3,
        fieldsToReturn = ["parent_folder", "file_name", "file_contents"]
    )
    # print(redisQueryResult)

    # Combine results of Redis Query and Return to CLI Agent
    combinedResult = ""
    resultFilePaths = []
    for result in redisQueryResult:
        combinedResult = result["file_contents"] + "\n"
        resultFilePaths.append(os.path.join(result["parent_folder"], result["file_name"]))

    # print("Combined Result File Contents: ", combinedResult)
    # print("Source Chunked Godot Docs File Paths: ", resultFilePaths)

    return combinedResult

async def main():
    await cliAgent.to_cli()

asyncio.run(main())