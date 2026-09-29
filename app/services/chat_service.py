from app.agent.agent import ask_agent

def chat(message: str):

    response = ask_agent(message)

    return {
        "response": response
    }