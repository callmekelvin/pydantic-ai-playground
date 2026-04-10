from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.usage import UsageLimits
from llamaCppModel import llama_cpp_model

from agents.scifiAgent import sciFiAgent
from agents.redditAgent import redditAgent, RedditQuery
import asyncio

instructions = """
You are a CLI Agent that will accept prompts from the user.

Return responses to the prompts the users provide.

Use the `scifi_agent` tool to assist answering any sci fi questions.
Use the `reddit_agent` tool to assist serving XYZ number of posts from the Technology Subreddit.
"""

cliAgent = Agent(
    model=llama_cpp_model,
    instructions=instructions,
    output_type=str
)

@cliAgent.tool
async def scifi_agent(ctx: RunContext[str]) -> str:
    print("SciFi Agent Triggered")

    result = await sciFiAgent.run(
        user_prompt=ctx.prompt.lower(),
        usage_limits=UsageLimits(request_limit=2)
    )
    # result = await sciFiAgent.run()

    return result.output

@cliAgent.tool
async def reddit_agent(ctx: RunContext[str]) -> dict:
    print("Reddit Agent Triggered")

    # Possible Improvement
    # Should use another Sub Agent to specifically parse the prompt and generate structured output for Reddit Sub Agent to consume
    # However, this is to show how the Dependencies work
    # https://pydantic.dev/docs/ai/core-concepts/output/

    sortType = str([st for st in ["best", "hot", "new", "top", "rising"] if st in ctx.prompt][0]) or "top"
    timeFilter = str([time for time in ["day", "month", "year"] if time in ctx.prompt][0]) or "day"

    redditQueryDeps = RedditQuery(
        subredditName="technology",
        sort=sortType,
        numOfPosts=10,
        timeFilter=timeFilter
    )

    # Pass in dependencies used by Agent
    result = await redditAgent.run(
        deps=redditQueryDeps
    )

    return result.output

async def main():
    await cliAgent.to_cli()

asyncio.run(main())