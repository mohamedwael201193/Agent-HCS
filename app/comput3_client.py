import os
import httpx
from dotenv import load_dotenv

load_dotenv()

COMPUT3_API_KEY = os.getenv("COMPUT3_API_KEY")
COMPUT3_API_BASE = "https://api.comput3.ai/v1"

async def analyze_contract(contract_code: str):
    headers = {
        "Authorization": f"Bearer {COMPUT3_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""You are an expert smart contract auditor. Analyze the following Solidity smart contract code for vulnerabilities, security flaws, and potential exploits. Provide a detailed report of any findings, including severity and recommendations for remediation. If no vulnerabilities are found, state that clearly.

Smart Contract Code:
```solidity
{contract_code}
```

Audit Report:"""

    payload = {
        "model": "llama3:70b",  # Or a similar powerful model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{COMPUT3_API_BASE}/chat/completions", headers=headers, json=payload, timeout=300.0)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"Error during AI analysis: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        print(f"An error occurred while requesting: {e}")
        return f"Error during AI analysis: {e}"


