# Orchestration Agent

This is the main orchestration agent that coordinates between specialized sub-agents to provide comprehensive financial and lifestyle advice.

## Sub-Agents

1. **FI Money Agent**
   - Handles financial transactions, balances, and account management
   - Provides real-time financial data and account operations

2. **Lifestyle Agent**
   - Offers personalized financial lifestyle advice
   - Helps with budgeting, savings goals, and financial planning

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`)
- Environment variables configured (see `.env.example`)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update the values

### Usage

```python
from orchestration.agent import OrchestrationAgent
import asyncio

async def main():
    # Initialize the orchestration agent
    orchestrator = OrchestrationAgent()
    
    # Example query
    response = await orchestrator.route_query("How can I save more money?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### `OrchestrationAgent`

Main class that coordinates between sub-agents.

#### Methods

- `__init__()`: Initializes the agent and loads sub-agents
- `load_sub_agents()`: Dynamically loads available sub-agents
- `route_query(user_query: str, context: Optional[Dict] = None) -> str`: Routes the query to appropriate sub-agent(s)

## Error Handling

The agent includes basic error handling for sub-agent loading and query routing. Errors are caught and returned in a user-friendly format.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
