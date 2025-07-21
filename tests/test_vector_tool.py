from app.agent.tools.vector_tool import vector_tool


def main():
    test_query = "Cosa è stato organizzato per l'anniversario della Cattolica?"

    result = vector_tool(query=test_query)

    print("=== TOOL OUTPUT ===")
    print(result)


if __name__ == "__main__":
    main()
