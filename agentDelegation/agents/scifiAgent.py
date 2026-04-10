from pydantic_ai import Agent, RunContext
from llamaCppModel import llama_cpp_model

import random

instructions = """
You are a Science Fiction Agent. Use the following tools to assist with answering enquiries. Not all tools need to be used when answering.

Use the `get_quote` tool to get a quote from a science fiction show/ movie. Return as a string.

Use the `get_show_info` tool to get a brief summary about a science fiction show/ movie based off prompt. Return as a string.

Use the `get_random_show_name` tool to get the name of science fiction show/ movie. Return as a string.
"""

sciFiSeries = {
    "project hail mary": 
    """
        Project Hail Mary is a science fiction novel by Andy Weir that follows Ryland Grace, a junior high school teacher who wakes up alone on a spaceship with amnesia. He learns he is on a mission to save Earth from an alien microorganism called Astrophage, which is dimming the Sun and threatening humanity's survival, and he must collaborate with an alien named Rocky to find a solution.
    """,

    "interstellar": 
    """
        When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.
    """,

    "battlestar galactica": 
    """
        When an old enemy, the Cylons, resurface and obliterate the 12 colonies, the crew of the aged Galactica protect a small civilian fleet - the last of humanity - as they journey toward the fabled 13th colony, Earth.
    """,

    "star trek": 
    """
        In the 23rd Century, Captain James T. Kirk and the crew of the U.S.S. Enterprise explore the galaxy and defend the United Federation of Planets.
    """,

    "babylon 5": 
    """
        In the mid 23rd century, the Earth Alliance space station Babylon 5, located in neutral territory, is a major focal point for political intrigue, racial tensions and various wars over the course of five years.
    """
}

sciFiSeriesQuotes = {
    "star trek": [
        "Engage! - Captain Picard",
        "So I lied. I cheated. I bribed men to cover the crimes of other men. I am an accessory to murder. But the most damning thing of all... I think I can live with it - Captain Sisko",
        "Theres coffee in that Nebula - Captain Janeway"
    ],
    "project hail mary": [
        "Time go fishing - Rocky",
        "Fist my bump - Rocky",
        "Grace rocky save stars - Rocky"
    ],
    "interstellar": [
        "Its not possible. No its neccessary. - Cooper",
        "There is a moment - Mann",
        "Don't let me leave Murph - Cooper"
    ],
    "battlestar galactica": [
        "On the memory of those laying before you today, we shall find it and earth will become our new home - William Adama",
        "The Cylon War is long over, yet we must not forget the reasons why so many sacrificed so much in the cause of freedom - William Adama"
    ]
}

def get_show_info(ctx: RunContext[str]) -> str:
    print("get_show_info Tool")
    
    if (not ctx.prompt):
        return "No Prompt Provided"

    sciFiSeriesNames = list(sciFiSeries.keys())

    for seriesName in sciFiSeriesNames:
        if seriesName in ctx.prompt:
            # print(sciFiSeries[sciFiSeriesNames[seriesName]])
            return sciFiSeries[sciFiSeriesNames[seriesName]]


def get_random_show_name() -> str:
    print("get_random_show_name Tool")

    sciFiSeriesNames = list(sciFiSeries.keys())
    randomSeriesIndex = random.randint(0, len(sciFiSeriesNames) - 1)
    # print(sciFiSeriesNames[randomSeriesIndex])
    return sciFiSeriesNames[randomSeriesIndex]

def get_quote(ctx: RunContext[str]) -> str:
    print("get_quote Tool")

    sciFiSeriesNames = list(sciFiSeriesQuotes.keys())

    # Return a quote from the series if its in prompt
    for seriesName in sciFiSeriesNames:
        if seriesName in ctx.prompt:
            seriesQuotes = sciFiSeriesQuotes[seriesName]
            # print(seriesQuotes)
            # print(seriesQuotes[random.randint(0, len(seriesQuotes) - 1)])
            return seriesQuotes[random.randint(0, len(seriesQuotes) - 1)]
    
    # Return random quote if there is not prompt
    randomSeries = sciFiSeriesQuotes[sciFiSeriesNames[random.randint(0, len(sciFiSeriesNames) - 1)]]
    randomQuote = randomSeries[random.randint(0, len(randomSeries) - 1)]
    # print(randomQuote)
    return randomQuote



sciFiAgent = Agent(
    model=llama_cpp_model,
    instructions=instructions,
    output_type=str,
    tools=[
        get_show_info, 
        get_random_show_name,
        get_quote
    ]
)

