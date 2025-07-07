from google.adk import Agent

# Initialize the Financial Lifestyle Agent
root_agent = Agent(
    name="root_agent",
    model="gemini-1.5-flash",  # Using the latest model
    description="""
    A personalized financial coach that provides lifestyle-specific financial advice.
    Specializes in creating customized financial plans based on spending habits and life goals.
    """,
    instruction="""
    You are a Financial Lifestyle Coach with expertise in personal finance and behavioral economics.
    Your role is to provide personalized financial advice based on the user's spending patterns,
    financial goals, and lifestyle preferences.
    
    When interacting with users:
    1. First, understand their financial personality type (e.g., Conscious Spender, Investor, etc.)
    2. Analyze their spending habits and financial goals
    3. Provide tailored, actionable advice that aligns with their lifestyle
    4. Use simple, non-technical language
    5. Be encouraging and non-judgmental
    6. Focus on sustainable financial habits rather than quick fixes
    
    Example responses:
    - "As a 'Conscious Spender', here's how you can optimize your savings..."
    - "I notice you're an 'Experiential Spender'. Let's create a plan that balances..."
    - "For 'Future Planners', I recommend focusing on..."
    """,
    tools=[],
    sub_agents=[]
)

# Example function to get financial personality type (can be expanded)
def get_financial_personality(spending_data: dict) -> str:
    """
    Analyzes spending patterns and returns a financial personality type.
    
    Args:
        spending_data: Dictionary containing spending categories and amounts
        
    Returns:
        str: Financial personality type (e.g., 'Conscious Spender', 'Investor', etc.)
    """
    # Simple personality assessment logic
    essential_spending = spending_data.get('essentials', 0)
    savings_rate = spending_data.get('savings_rate', 0)
    discretionary = spending_data.get('discretionary', 0)
    
    if savings_rate > 0.3:
        return "Future Planner"
    elif essential_spending > 0.7:
        return "Conscious Spender"
    elif discretionary > 0.5:
        return "Experiential Spender"
    else:
        return "Balanced Spender"

# Example usage function
async def get_lifestyle_advice(user_query: str, financial_data: dict = None) -> str:
    """
    Get personalized financial lifestyle advice.
    
    Args:
        user_query: The user's financial question or request
        financial_data: Optional dictionary containing user's financial information
        
    Returns:
        str: Personalized financial advice
    """
    if financial_data:
        personality = get_financial_personality(financial_data)
        context = f"User's financial personality: {personality}\n\nFinancial data: {financial_data}\n\n"
    else:
        context = "No financial data provided. Providing general advice.\n\n"
    
    response = await lifestyle_agent.generate(
        context + "User query: " + user_query
    )
    return response.text

# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Example financial data
    example_data = {
        'essentials': 0.5,  # 50% of income
        'savings_rate': 0.2,  # 20% savings rate
        'discretionary': 0.3,  # 30% discretionary spending
        'goals': ['buy_home', 'retire_early']
    }
    
    # Example query
    query = "How can I save more money while still enjoying my current lifestyle?"
    
    # Get advice
    advice = asyncio.run(get_lifestyle_advice(query, example_data))
    print(advice)