import asyncio
import os
from flask import Flask, request, jsonify, render_template
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import json
from datetime import datetime

from app.hedera_client import create_audit_topic, submit_audit_log
from app.comput3_client import analyze_contract

load_dotenv()

app = Flask(__name__)
mcp_server = FastMCP(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/audit", methods=["POST"])
async def audit():
    data = await request.get_json()
    contract_code = data.get("contract_code")

    if not contract_code:
        return jsonify({"error": "No contract code provided"}), 400

    try:
        # 1. Create a new HCS topic for this audit
        topic_id = await create_audit_topic()

        # 2. Log the initial action
        init_log = {"step": 1, "action": "AUDIT_INITIATED", "timestamp": datetime.utcnow().isoformat()}
        await submit_audit_log(topic_id, json.dumps(init_log))

        # 3. Perform AI analysis via Comput3.ai
        analysis_result = await analyze_contract(contract_code)

        # 4. Log the final result
        final_log = {"step": 2, "action": "ANALYSIS_COMPLETE", "result": analysis_result, "timestamp": datetime.utcnow().isoformat()}
        await submit_audit_log(topic_id, json.dumps(final_log))

        # 5. Return a user-friendly summary
        return jsonify({
            "analysis": analysis_result,
            "audit_trail_id": topic_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mcp_server.tool()
async def auditContract(contract_address: str, contract_code: str):
    # This logic is identical to the /api/audit endpoint
    # Create Hedera Topic
    topic_id = await create_audit_topic()
    if not topic_id:
        return "Failed to create Hedera topic"

    # Log audit initiation
    await submit_audit_log(topic_id, f"MCP Audit initiated for contract: {contract_address} - {contract_code[:100]}...")

    # Analyze contract with AI
    ai_analysis_result = await analyze_contract(contract_code)
    if not ai_analysis_result:
        return "AI analysis failed"

    # Log AI analysis result
    await submit_audit_log(topic_id, f"MCP AI analysis complete. Result: {ai_analysis_result[:100]}...")

    return f"Audit Summary: {ai_analysis_result}\nVerifiable Hedera Topic ID: {topic_id}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


