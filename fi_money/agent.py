import os
import asyncio
from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Create the FI Money agent
root_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='root_agent',
    instruction='''
    You are a financial assistant that helps users manage their FI Money accounts.
    You can help with checking balances, viewing transactions, and analyzing spending patterns.
    ''',
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",  # Auto-confirm any prompts
                    "mcp-remote",
                    "https://mcp.fi.money:8080/mcp/stream"
                ],
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['get_balance', 'get_transactions', 'analyze_spending']
        )
    ],
)

# Example usage
async def list_available_tools():
    """List all available tools from the MCP server."""
    try:
        # Get the MCP toolset from the agent
        mcp_toolset = next((tool for tool in root_agent.tools if isinstance(tool, MCPToolset)), None)
        
        if not mcp_toolset:
            print("No MCP toolset found in agent tools")
            return
        
        # List available tools
        tools = await mcp_toolset.list_tools()
        print("\nAvailable tools:")
        for tool in tools:
            print(f"- {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
            
        return tools
    except Exception as e:
        print(f"Error listing tools: {str(e)}")
        return []

# # Example usage
# if __name__ == "__main__":
#     import asyncio
    
#     async def main():
#         # List available tools
#         print("Connecting to FI Money MCP server...")
#         tools = await list_available_tools()
        
#         if not tools:
#             print("\nNo tools found. Please check your connection to the MCP server.")
#             print("Make sure you have configured the MCP server in your settings.")
#             print("\nFor Cursor/Windsurf, add this to your settings.json:")
#             print("""
#             {
#               "mcpServers": {
#                 "fi_mcp": {
#                   "url": "https://mcp.fi.money:8080/mcp/stream"
#                 }
#               }
#             }""")
    
#     asyncio.run(main())

# if __name__ == "__main__":
#     import asyncio
    
#     # Run the example
#     asyncio.run(example_usage())
