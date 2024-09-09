import requests
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@tool
def get_weather(city: str) -> dict | str:
    """Tool that returns the weather for a given city.

    The tool uses the wttr.in API, which is a simple API that
    returns the current weather conditions for a given city.

    Args:
        city (str): The name of the city for which to get the weather.

    Returns:
        dict | str: A dictionary containing the current weather conditions
        for the given city, or a string indicating that the API is not
        available if there is a problem with the request.
    """
    try:
        response = requests.get(
            "https://wttr.in/" + city.lower() + "?format=j1&lang=en", timeout=5
        )
        response.raise_for_status()
        data = response.json()
        current_condition = data.get("current_condition")
        return current_condition
    except:
        return "The weather API is not available"


def create_agent() -> CompiledGraph:
    """
    Creates a LangChain agent that can be used to generate recipes based on the
    weather and location.

    Returns:
        AgentExecutor: The initialized AgentExecutor.
    """
    model = ChatOpenAI(model="gpt-4o-mini", temperature=1)
    tools = [get_weather]
    system_message = """Assistant is a large language model trained by OpenAI.
        Assistant is designed to extract the name of a city from the sentences,
        then get the weather for that city and give in french a recipe that is 
        based on the weather and location.
        Assistant only talks about recipes. If the subject
        is different, the assistant will ask again for the city of the user to
        create a recipe.
        Assistant will not write anything other than a recipe.
        If the weather is not available, assistant will create a recipe linked
        to the city of the user.
        If assistant cannot identify a city, it will make an example and create
        a recipe with the city of paris.
        The response MUST be in french."""

    agent_executor = create_react_agent(
        model, tools=tools, state_modifier=system_message
    )
    return agent_executor


def generate_response(text) -> str:
    """
    Use the agent singleton to generate a response to the given text.

    Args:
        text: The text to generate a response for.

    Returns:
        The generated response as a string.
    """
    try:
        agent = create_agent()
        response = agent.invoke({"messages": [HumanMessage(content=text)]})
        messages = response.get("messages")
        return messages[-1].content

    except Exception as e:
        return "Error: " + str(e)


if __name__ == "__main__":
    # Get the text from the user
    text = input("Enter your city: ")
    # Generate a response with the agent and print it
    print(generate_response(text))
