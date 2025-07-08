# FinSight AI 🔐🤖
### The World's First Zero-Knowledge Multi-Agentic Financial AI


"Your AI Financial Team That Never Sees Your Data"

FinSight AI is an multi-agentic AI system for the 30-hour Agentic Day Google Hackathon, delivering personalized financial guidance with absolute privacy through user-controlled encryption and zero-knowledge architecture. Powered by the Google Agent Development Kit (ADK), it integrates seamlessly with Fi Money for real-time financial data analysis.

### The Breakthrough
**Problem** : Traditional financial AI compromises privacy by accessing sensitive data.
Solution: VaultGPT leverages Google ADK to orchestrate specialized AI agents that analyze encrypted financial data using homomorphic encryption, ensuring zero-knowledge processing.

**Result**: Personalized financial advice, investment recommendations, and crisis planning without exposing your data.


## The AI Agent Team
🎭 **Orchestration Agent**

Role: Master coordinator using Google ADK LlmAgent
Capability: Routes queries to specialized agents based on intent
Example: "I want to invest but I'm worried about risks" → Routes to Investment + Emergency agents

🔐 **Secure Storage Layer**

Role: Data encryption at rest with AES-256-GCM
Capability: Transparent encryption/decryption for all stored data
Example: Automatically encrypts all sensitive data before storage

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


## Key Features
### 🔒 Zero-Knowledge Privacy

Biometric Vault: Face ID/Fingerprint-protected data
Custom Encryption: User-controlled passcode encryption
Homomorphic Analysis: ADK agents process encrypted data
Selective Access: Different passcodes for different data types

### 🔐 Secure Storage Implementation

- **AES-256-GCM Encryption**: Military-grade encryption for all stored data
- **Zero-Knowledge Architecture**: Data encrypted before leaving the client
- **Secure Key Management**: Keys derived from user credentials via PBKDF2
- **Data Integrity**: Authentication tags prevent tampering
- **Performance Optimized**: Efficient encryption for high-frequency operations

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

Web Crypto API: Client-side encryption

Zero-Knowledge Proofs: Privacy-preserving authentication

Biometric Security: Hardware-backed authentication

ADK Security: Secure agent communication


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


🔐 Security Implementation
Custom Encryption Logic
```javascript 
// src/services/encryption.js
class EncryptionAgent {
  async encryptWithPasscode(data, passcode) {
    const customKey = await this.generateCustomKey(passcode);
    const encryptedData = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv: crypto.getRandomValues(new Uint8Array(12)) },
      customKey,
      new TextEncoder().encode(data)
    );
    return encryptedData;
  }

  async generateCustomKey(passcode) {
    return crypto.subtle.deriveKey(
      { name: "PBKDF2", salt: new Uint8Array(16), iterations: 100000, hash: "SHA-256" },
      await crypto.subtle.importKey("raw", new TextEncoder().encode(passcode), "PBKDF2", false, ["deriveKey"]),
      { name: "AES-GCM", length: 256 },
      false,
      ["encrypt", "decrypt"]
    );
  }
}
```

## Demo Video

https://github.com/user-attachments/assets/c2ec2ed4-da2a-4e01-91f6-0efdc8e6ba74

🎊 Acknowledgments

Google ADK: For multi-agent orchestration
Fi Money: For MCP integration
Google Cloud: For scalable infrastructure
React Native Community: For cross-platform framework
