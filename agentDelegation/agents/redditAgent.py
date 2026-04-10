from pydantic import BaseModel
from typing import Literal, Annotated, Optional
from pydantic_ai import Agent, RunContext
from llamaCppModel import llama_cpp_model

import requests

# Pydantic Base Model to enforce validation and model
class RedditQuery(BaseModel):
    subredditName: Optional[str]
    sort: Optional[Literal["best", "hot", "new", "top", "rising"]]
    numOfPosts: Optional[Annotated[int, "lt=100"]]
    timeFilter: Optional[Literal["day", "month", "year"]]

instructions = """
Get Reddit Posts (Headlines) from Reddit Subreddit Forums
"""

def retrieve_headlines_from_reddit(ctx: RunContext[RedditQuery]) -> dict:
    # Retrieve settings to make request from Agent Dependencies (ctx.deps). If unable to obtain, set request to defaults
    reddit_url = f"https://www.reddit.com/r/{ctx.deps.subredditName}/{ctx.deps.sort}.json?limit={ctx.deps.numOfPosts}&t={ctx.deps.timeFilter}"
    # print(reddit_url)

    res = requests.get(reddit_url)

    if not (200 <= res.status_code < 300):
        print("Network Error Retrieving Reddit Posts from this Subreddit")
        return "Network Error Retrieving Reddit Posts from this Subreddit"

    jsonRes = res.json()

    redditHeadlines = {}
    headlineNo = 0
    for child in jsonRes["data"]["children"]:
        redditHeadlines[headlineNo] = child["data"]["title"]
        headlineNo += 1
    
    return redditHeadlines

redditAgent = Agent(
    model=llama_cpp_model,
    instructions=instructions,
    output_type=dict,
    deps_type=RedditQuery, # Specify Dependencies used by the Agent
    tools=[
        retrieve_headlines_from_reddit
    ]
)

