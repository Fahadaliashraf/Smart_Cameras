import warnings
import subprocess
import pandas as pd
from langchain_ollama import OllamaLLM
 # Updated import
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain import hub
import socket

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langsmith.client")

# Function to check if a port is open (means server is running)
def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

# 1. Start Ollama Server if not running
if not is_port_open("127.0.0.1", 11434):
    print("Starting Ollama server...")
    subprocess.Popen(["ollama", "serve"])

# 2. Pull model if needed
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
    if "llama3.2" not in result.stdout:
        print("Model not found, pulling...")
        subprocess.run(["ollama", "pull", "llama3.2"], check=True)
    else:
        print("Model already available.")
except Exception as e:
    print(f"Error checking/pulling model: {str(e)}")

# 3. Load Ollama model using OllamaLLM
try:
    llm = OllamaLLM(  # Using OllamaLLM instead of Ollama
        model="llama3.2",
        temperature=0.3,
        timeout=240
    )
except Exception as e:
    raise RuntimeError(f"Failed to load Ollama model: {str(e)}")

# 4. Define CSV tools
def read_logs(_):
    try:
        df = pd.read_csv("detection_logs.csv")
        return df.head().to_string()
    except Exception as e:
        return f"Error reading logs: {str(e)}"

def search_logs(term):
    try:
        df = pd.read_csv("detection_logs.csv")
        matches = df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)
        return f"Found {matches.sum()} entries containing '{term}'."
    except Exception as e:
        return f"Error searching logs: {str(e)}"

# 5. Define Tools List
tools = [
    Tool(
        name="Read Detection Logs",
        func=read_logs,
        description="Use this tool to read the first few rows of detection logs."
    ),
    Tool(
        name="Search Detection Logs",
        func=search_logs,
        description="Use this tool to search for specific terms in detection logs."
    )
]

# 6. Create agent
try:
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
except Exception as e:
    raise RuntimeError(f"Failed to create agent: {str(e)}")

# 7. Question loop
while True:
    try:
        user_query = input("\nYour question (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break

        response = agent_executor.invoke({"input": user_query})
        print("\n🤖 Answer:", response['output'])

    except Exception as e:
        print(f"\n⚠️ Error processing your request: {str(e)}")
        print("Please try again.")