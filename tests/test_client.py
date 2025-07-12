# activate the venv with source $(poetry env info --path)/bin/activate

import sys
import os

from app.agent.client import get_model

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.messages import HumanMessage, AIMessage


def test_model_response():
    print("Inizializzazione del modello...")
    model = get_model()

    print("Invio richiesta...")
    test_message = [HumanMessage(content="Chi sono io?")]
    response = model.invoke(test_message)

    assert isinstance(response, AIMessage), "La risposta non è un AIMessage!"
    assert response.content.strip() != "", "La risposta è vuota!"

    print("Test passato")
    print("\nRisposta del modello:")
    print(response.content)


if __name__ == "__main__":
    test_model_response()