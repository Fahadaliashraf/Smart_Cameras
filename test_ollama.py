import ollama
import asyncio

async def test_ollama_chat():
    """Tests the ollama.chat API for a simple interaction."""
    try:
        response = await ollama.chat(
            model='llama3.2:latest',  # Replace with your desired model
            messages=[
                {
                    'role': 'user',
                    'content': 'Write a short poem about a cat.',
                },
            ]
        )
        if response and response.message and response.message.content:
            print("Chat Test Successful:")
            print(response.message.content)
        else:
            print("Chat Test Failed: Unexpected response format.")
            print(response)
    except ConnectionError as e:
        print(f"Chat Test Failed (Connection Error): {e}")
        print("Please ensure Ollama is running and accessible.")
    except Exception as e:
        print(f"Chat Test Failed (General Error): {e}")
        print(f"Error details: {e}")

async def test_ollama_list():
    """Tests the ollama.list API to retrieve installed models."""
    try:
        models_response = await ollama.list()
        if models_response and models_response.models:
            print("\nList Models Test Successful:")
            for model in models_response.models:
                print(f"- {model.name}:{model.tag}")
        else:
            print("List Models Test Failed: Unexpected response format.")
            print(models_response)
    except ConnectionError as e:
        print(f"List Models Test Failed (Connection Error): {e}")
        print("Please ensure Ollama is running and accessible.")
    except Exception as e:
        print(f"List Models Test Failed (General Error): {e}")
        print(f"Error details: {e}")

async def main():
    print("Starting Ollama Python Library Tests...")
    await test_ollama_chat()
    await test_ollama_list()
    print("\nOllama Tests Completed.")

if __name__ == "__main__":
    asyncio.run(main())