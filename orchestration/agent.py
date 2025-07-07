import os
import asyncio
from typing import Dict, Any, List, Optional
from google.adk import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv
import importlib.util
import sys

# Load environment variables
load_dotenv()

# Add parent directory to path to allow relative imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import sub-agents
from fi_money.agent import root_agent as fi_money_agent
from lifestyle.agent import root_agent as lifestyle_agent

# Initialize the Orchestration Agent
root_agent = Agent(
    name="orchestration_agent",
    model="gemini-1.5-flash",
    description="""
    A master agent that coordinates between specialized sub-agents to provide
    comprehensive financial and lifestyle management services.
    """,
    instruction="""
    You are an orchestration agent that coordinates between specialized sub-agents.
    Your role is to route user queries to the appropriate sub-agents and combine their responses.
    
    Available sub-agents:
    1. fi_money: Handles financial transactions, balances, and account management
    2. lifestyle: Provides personalized financial lifestyle advice and planning
    
    When handling queries:
    - For financial transactions or account queries, use the fi_money agent
    - For financial planning, lifestyle advice, or spending analysis, use the lifestyle agent
    - For complex queries that involve both, route to both agents and combine their responses
    - Always ensure responses are clear about which agent provided which information
    """,
    tools=[],
    sub_agents=[fi_money_agent, lifestyle_agent]
)

async def route_query(user_query: str, context: Optional[Dict] = None) -> str:
    """
    Route the user query to the appropriate sub-agent(s) and return the response.
    
    Args:
        user_query: The user's query
        context: Optional context dictionary containing additional information
        
    Returns:
        str: The response from the relevant agent(s)
    """
    context = context or {}
    responses = []
    
    # Simple routing logic
    query_lower = user_query.lower()
    
    # Check which agent should handle the query
    fi_money_keywords = ['balance', 'transaction', 'account', 'transfer', 'pay', 'deposit', 'withdraw']
    lifestyle_keywords = ['advice', 'plan', 'budget', 'save', 'spend', 'invest', 'goal', 'lifestyle']
    
    if any(keyword in query_lower for keyword in fi_money_keywords):
        responses.append(f"[FI Money Agent] This would handle: {user_query}")
    elif any(keyword in query_lower for keyword in lifestyle_keywords):
        responses.append(f"[Lifestyle Agent] This would provide advice for: {user_query}")
    else:
        response = await root_agent.generate_response(user_query)
        responses.append(f"[Orchestration Agent] {response}")
    
    # Combine responses
    return "\n\n".join(responses)

# Example usage
if __name__ == "__main__":
    async def run_example():
        # Example queries
        queries = [
            "What's my current account balance?",
            "How can I improve my spending habits?",
            "What's my net worth and how can I grow it?"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            response = await route_query(query)
            print(f"Response: {response}")
    
    # Run the example
    asyncio.run(run_example())
