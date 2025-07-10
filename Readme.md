# FinSight AI 🔐🤖
### Secure Multi-Agentic Financial AI with ADK Sandboxing

"Your AI Financial Team with Enterprise-Grade Security"

FinSight AI is a multi-agentic AI system for the 30-hour Agentic Day Google Hackathon, delivering personalized financial guidance with robust security through Google ADK's sandboxing and zero-persistence architecture. It integrates seamlessly with Fi Money for real-time financial data analysis while maintaining the highest security standards.

### The Breakthrough
**Problem**: Traditional financial AI systems often expose sensitive data to security risks during processing.

**Solution**: FinSight leverages Google ADK's secure sandboxing to isolate and protect financial data processing, with a zero-persistence model that ensures no sensitive data remains after processing.

**Result**: Enterprise-grade security with personalized financial advice, investment recommendations, and crisis planning, all processed in a secure, isolated environment.


## The AI Agent Team
🎭 **Orchestration Agent**

Role: Master coordinator using Google ADK LlmAgent
Capability: Routes queries to specialized agents based on intent with built-in safety checks
Example: "I want to invest but I'm worried about risks" → Routes to Investment + Emergency agents with appropriate guardrails

🔐 **ADK Security Layer**

Role: Enforces security policies and manages sandboxed execution
Capability: Implements input/output validation, content filtering, and secure data handling
Example: Validates all agent operations and enforces data access controls

💰 **Financial Advisor Agent**

Role: Personalized financial coach
Capability: Prompt-tuned for lifestyle-specific advice using ADK
Example: "As a 'Conscious Spender,' here's your savings plan"

🚨 **Emergency Agent**

Role: Crisis financial advisor
Capability: Handles high-pressure scenarios with ADK-driven logic
Example: "Job loss detected - here's your 90-day survival plan"

💰 **Fi Money Agent**

Role: Financial data integration specialist
Capability: Connects to Fi Money MCP for real-time banking data
Example: "Your current balance across all accounts is ₹1,24,567.89"

📊 **Analytics Agent**

Role: Data scientist for predictions
Capability: Analyzes Fi MCP data for financial insights
Example: "Your credit score will reach 750 by December"

📈 **Real Time Investment Agent**

Role: Real-time market advisor
Capability: Integrates Google Search API for live market data
Example: "SBI Small Cap fund dropped 3% today - good entry point"


## Security Approach

### 🛡️ Multi-Layered Security Architecture

- **Device Access**: Biometric + Passcode
- **Data Encryption**: Web Crypto API
- **Prompt Safety**: ADK Built-in protections
- **Content Filtering**: ADK Built-in content moderation
- **Data Persistence**: Zero Persistence + ADK Sandboxing
- **Session Security**: ADK Session Management with TTL
- **Identity Management**: ADK Auth + OAuth integration
- **Code Execution**: ADK Sandboxed Environment
- **Network Security**: ADK VPC-SC perimeters
- **UI Safety**: ADK Content Escaping and sanitization

## Key Features
### 🔒 ADK-Powered Security

- **Sandboxed Execution**: Each agent runs in isolated environments using ADK's sandboxing
- **Zero-Persistence Model**: No sensitive data remains after processing
- **Input/Output Guardrails**: Built-in content filtering and validation
- **Secure Session Management**: Automatic cleanup after TTL expiry
- **VPC-SC Perimeters**: Network-level isolation for data protection

### 🔐 Secure Processing Architecture

- **ADK Sandboxing**: Isolated execution environments for all agents
- **Temporary Data Handling**: In-memory processing only during active sessions
- **Secure Data Flow**: End-to-end encryption for all communications
- **Automatic Cleanup**: Complete data wipe after session expiry
- **Compliance Ready**: Built to meet enterprise security standards

### 🧠 Multi-Agent Intelligence

- **ADK Orchestration**: LlmAgent routes queries efficiently
- **Collaborative Workflow**: Sequential and Parallel agents for complex tasks
- **Context Sharing**: ADK session state maintains conversation continuity
- **Specialized Expertise**: Each agent trained for specific financial domains
- **Secure Data Flow**: All data access goes through the secure storage layer

### 📱 Fi Money Integration

The Fi Money Agent provides seamless integration with Fi Money's MCP platform, offering:

- **Complete API Coverage**: Access to all 4 MCP endpoints:
  - Account balances and transactions
  - Credit score and history
  - EPF and retirement data
  - Net worth analysis
- **Real-Time Data Sync**: Live financial data with configurable refresh rates
- **Secure Authentication**: OAuth 2.0 with token refresh
- **Local Caching**: Optimized performance with intelligent data caching
- **Error Resilience**: Automatic retries and graceful degradation

### 🎯 Personalized Guidance

Financial Personality: AI-driven behavioral analysis

Lifestyle Coaching: Tailored advice for life stages

Crisis Management: Emergency-specific guidance

Predictive Insights: Future projections using ADK analytics


## 🛠️ Tech Stack
### Frontend

React Native + Expo: Cross-platform mobile app

TailwindCSS: Utility-first styling

Biometric APIs: Face ID/Fingerprint authentication

Voice Interface: Speech-to-text integration

### Backend

Node.js + Express: RESTful API server

Google ADK (Python): Multi-agent system

Google Cloud Functions: Serverless compute

Fi MCP SDK: Financial data integration

### AI/ML

Google ADK: Agent orchestration with Gemini-2.0-pro

Custom Prompts: Specialized agent instructions

TensorFlow.js: Client-side ML inference

Google Search API: Real-time market data

### Security

- **ADK Sandboxing**: Isolated execution environments with strict resource constraints

- **Zero-Persistence Model**: No sensitive data retention after session expiry

- **Content Safety**: Built-in content filtering and moderation

- **Network Security**: VPC-SC perimeters for data isolation

- **Session Management**: Automatic cleanup with configurable TTL

- **Input Validation**: Protection against injection and prompt attacks

- **Compliance**: Built to meet enterprise security standards


### Cloud Infrastructure

Google Cloud Platform: Scalable infrastructure

Vertex AI: ADK deployment

Firebase: Real-time database

Cloud Storage: Encrypted data persistence


## Getting Started
Prerequisites

Python 3.10+ and Node.js 18+

React Native development environment

Google Cloud account with Vertex AI API enabled

Fi Money account with connected financial accounts


Installation
## Clone the repository
```bash 
git clone https://github.com/your-team/vaultgpt.git
cd vaultgpt

# Install Node.js dependencies
npm install

# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install google-adk
```
## Set up environment variables
```bash
cp .env.example .env
```
## Start Node.js server
```bash
npm run dev
```
## Start ADK service(for local testing) 
```python 
adk web
```
### Environment Variables
```bash
# Fi MCP Integration
FI_MCP_API_KEY=your_fi_api_key
FI_MCP_BASE_URL=https://api.fi.money

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_SEARCH_API_KEY=your_search_api_key
GOOGLE_CLOUD_CREDENTIALS=path/to/credentials.json

# ADK and Gemini
GOOGLE_GENAI_USE_VERTEXAI=True
GEMINI_API_KEY=your_gemini_api_key

# Security
ENCRYPTION_SECRET=your_encryption_secret
JWT_SECRET=your_jwt_secret
```

## 🎯 Agent Development Guide
Creating a New Agent
Each agent is defined in its own folder with agent.py, tools.py, and __init__.py. Here's an example for the Investment Agent:
investment/__init__.py
### This file makes the folder a Python package

investment/agent.py
```python
from google.adk import Agent, tool
from .tools import get_stock_price

class InvestmentAgent(Agent):
    name = "investment_agent"
    model = "gemini-2.0-pro"
    instructions = "Analyze market data and provide investment advice."
    tools = [get_stock_price]
```
investment/tools.py
```python
import requests
  
@tool
def get_stock_price(ticker: str) -> float:
    # Replace with actual API call
    response = requests.get(f"https://api.example.com/stock/{ticker}")
    data = response.json()
    return data['price']
```
Orchestration Integration

The Orchestration Agent routes queries to the appropriate subagents. Here's how it's structured:

orchestration/agent.py
```python
from google.adk import LlmAgent
from ..investment import InvestmentAgent
from ..emergency import EmergencyAgent

investment_agent = InvestmentAgent()
emergency_agent = EmergencyAgent()

orchestration_agent = LlmAgent(
    name="orchestration_agent",
    model="gemini-2.0-pro",
    instructions="Route user queries to the appropriate specialist agent.",
    sub_agents=[investment_agent, emergency_agent]
)
```

## Demo Video

https://github.com/user-attachments/assets/08ed1cad-1a17-485d-aefe-65a05f4c30ed

🎊 Acknowledgments

Google ADK: For multi-agent orchestration

Fi Money: For MCP integration

Google Cloud: For scalable infrastructure

React Native Community: For cross-platform framework
