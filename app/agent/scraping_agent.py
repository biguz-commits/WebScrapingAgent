from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.client import get_model
from app.agent.json_tool import get_unicatt_json


def main():

    llm = get_model()

    agent = llm.bind_tools([get_unicatt_json])

    system_prompt = SystemMessage(content=(
        "You are a helpful assistant for answering questions about the Università Cattolica website."
        " Use the `get_unicatt_json` tool **only** if the user asks about news, events or recent updates from the Unicatt website."
        " If the user asks general questions unrelated to Unicatt news, respond directly without calling any tool."
    ))

    question = input("Ask something about latest news in Unicatt website: ")
    user_message = HumanMessage(content=question)

    response = agent.invoke([system_prompt, user_message])

    print("\n📣 Response:")
    print(response.content)

if __name__ == "__main__":
    main()
