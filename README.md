# Agent HCS - The Verifiable AI Auditor

An MCP server that empowers the Aya AI agent to conduct AI-driven smart contract security audits with a verifiable, immutable audit trail on the Hedera Consensus Service.

🚀 Live Demo

🎥 Video Walkthrough

[Link to the 3-minute demo video]

Problem Statement

Smart contract vulnerabilities pose a significant risk in the Web3 ecosystem, leading to massive financial losses. While manual audits are effective, they are slow and expensive. Existing automated tools often lack transparency, producing "black box" results that are difficult to verify. Users and developers need a fast, accessible, and trustworthy way to perform security checks.

Our Solution: Agent HCS

Agent HCS solves this by integrating three powerful technologies:

Model Context Protocol (MCP): Exposes a powerful auditContract tool directly to AI agents like the one in the Aya Wallet.

Decentralized AI Compute (Comput3.ai): Leverages large-scale, specialized AI models for deep code analysis to identify complex vulnerabilities.

Decentralized Trust (Hedera Consensus Service): Creates an immutable, timestamped, and publicly verifiable audit trail for every step of the analysis process.

When a user requests an audit, Agent HCS logs the request to HCS, sends the code for AI analysis, and logs the result back to HCS, returning the final report and a link to the on-chain audit trail.

Technology Stack

Backend: Python, Flask, MCP SDK

AI Compute: Comput3.ai API

Blockchain: Hedera Consensus Service (via Hedera Python SDK)

Frontend: HTML, Tailwind CSS, JavaScript

Deployment: Vercel

How to Run Locally

**Clone the repository:**bash

git clone [repository_url]

cd agent-hcs





Set up a virtual environment:



Bash



python -m venv venvsource venv/bin/activate

Install dependencies:



Bash



pip install -r requirements.txt

Create a .env file in the /app directory with your credentials:



HEDERA_ACCOUNT_ID="0.0.6755516"

HEDERA_PRIVATE_KEY="0x4b1229f867735ff15ae6db58021c878c86965b70377d59b1b6148ab457ed3522"

COMPUT3_API_KEY="c3_api_E6vj04M2P5OoCuQ7x0QELZbI"

Run the application:



Bash



flask --app app/server.py run



Final Actions: Ensure environment variables are set in the Vercel project settings.

