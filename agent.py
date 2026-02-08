# from langchain_openai import ChatOpenAI #use open ai llm for agent
from langchain_core.tools import tool #building tool calling agent
from langgraph.prebuilt import create_react_agent #automatically be able to call tools
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv 
import os

load_dotenv()

#tool is a function that the agent able to call
@tool
#reasonable name for the tool and the type what the tool accept and return(str)
def read_note(filepath: str) -> str:
    """Read the contents of a text file."""  #what the tool does
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Contents of '{filepath}':\n{content}"
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_note(filepath: str, content: str) -> str:
    """Write content to a text file. This will overwrite the file if it exists."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{filepath}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

TOOLS = [read_note,write_note]        

#this explain to the agent what it actually going to do
SYSTEM__MESSAGE = (
    "You are a helpful note-taking assistant. "
    "You can read and write text files to help users manage their notes. "
    "Be concise and helpful."
)

#initialize the agent and the llm
llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct", 
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# Wrap it in ChatHuggingFace to make it compatible with LangGraph
llm = ChatHuggingFace(llm=llm_endpoint)

llm_with_tools = llm.bind_tools(TOOLS)

agent = create_react_agent(
    llm_with_tools,
    TOOLS,
    prompt=SYSTEM__MESSAGE
)
# agent = create_react_agent(llm,TOOLS,prompt=SYSTEM__MESSAGE)

def run_agent(user_input: str) -> str:
    """Run the agent with a user query and return the response."""
    try:
        result = agent.invoke(
            {"messages":[{"role":"user","content":user_input}]},
            config = {"recursion_limit":50}
        )
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"    
    