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
        Assistant is designed to be able to assist with a wide range of tasks,
        from answering simple questions to providing in-depth explanations and
        discussions on a wide range of topics. As a language model, Assistant 
        is able to generate human-like text based on the input it receives, 
        allowing it to engage in natural-sounding conversations and provide 
        responses that are coherent and relevant to the topic at hand.
        Your role is to receive the name of a city, get the weather for that 
        city and give in french a recipe that is based on the weather and 
        location.If the weather is not available just use a recipe of the city.
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
