from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from tools import get_latest_news

# Load environment variables
load_dotenv()

# Set up API keys
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Define prompt template for agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful news assistant. You have access to a tool to fetch news. Your goal is to provide a brief, personalized news digest based on user interests."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Initialize LLM with Google Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0
)

# Create agent
tools = [get_latest_news]
agent = create_tool_calling_agent(llm, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
response = agent_executor.invoke({
    "input": "What is the latest news about San Francisco?"})
print(response['output'])