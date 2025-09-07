import asyncio
import os
from flask import Flask, request, jsonify, render_template
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from app.hedera_client import create_audit_topic, submit_audit_log
from app.comput3_client import analyze_contract

load_dotenv()

app = Flask(__name__)
mcp_server = FastMCP(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/audit', methods=['POST'])
async def api_audit():
    contract_code = request.json.get('contract_code')
    if not contract_code:
        return jsonify({'error': 'No contract code provided'}), 400

    # Create Hedera Topic
    topic_id = await create_audit_topic()
    if not topic_id:
        return jsonify({'error': 'Failed to create Hedera topic'}), 500

    # Log audit initiation
    await submit_audit_log(topic_id, f'Audit initiated for contract: {contract_code[:100]}...')

    # Analyze contract with AI
    ai_analysis_result = await analyze_contract(contract_code)
    if not ai_analysis_result:
        return jsonify({'error': 'AI analysis failed'}), 500

    # Log AI analysis result
    await submit_audit_log(topic_id, f'AI analysis complete. Result: {ai_analysis_result[:100]}...')

    return jsonify({
        'ai_analysis': ai_analysis_result,
        'hedera_topic_id': topic_id
    })

@mcp_server.tool()
async def auditContract(contract_address: str, contract_code: str):
    # This logic is identical to the /api/audit endpoint
    # Create Hedera Topic
    topic_id = await create_audit_topic()
    if not topic_id:
        return "Failed to create Hedera topic"

    # Log audit initiation
    await submit_audit_log(topic_id, f'MCP Audit initiated for contract: {contract_address} - {contract_code[:100]}...')

    # Analyze contract with AI
    ai_analysis_result = await analyze_contract(contract_code)
    if not ai_analysis_result:
        return "AI analysis failed"

    # Log AI analysis result
    await submit_audit_log(topic_id, f'MCP AI analysis complete. Result: {ai_analysis_result[:100]}...')

    return f"Audit Summary: {ai_analysis_result}\nVerifiable Hedera Topic ID: {topic_id}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


