import os
import asyncio
from hedera import (
    Client,
    PrivateKey,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction,
    AccountId
)

# Configure the client for Hedera Testnet
client = None
try:
    operator_id_str = os.getenv("HEDERA_ACCOUNT_ID")
    operator_key_str = os.getenv("HEDERA_PRIVATE_KEY")

    if not operator_id_str or not operator_key_str:
        raise ValueError("HEDERA_ACCOUNT_ID and HEDERA_PRIVATE_KEY must be set in environment variables.")

    operator_id = AccountId.fromString(operator_id_str)

    # The private key might have a '0x' prefix, which the SDK doesn't expect.
    if operator_key_str.startswith('0x'):
        operator_key_str = operator_key_str[2:]
    
    operator_key = PrivateKey.fromString(operator_key_str)

    client = Client.forTestnet()
    client.setOperator(operator_id, operator_key)
except Exception as e:
    print(f"Error initializing Hedera client: {e}")
    client = None

async def create_audit_topic_async() -> str:
    """Creates a new HCS topic and returns the Topic ID as a string."""
    if not client:
        raise Exception("Hedera client is not initialized. Check environment variables.")

    transaction = TopicCreateTransaction()
    tx_response = await transaction.execute(client)
    receipt = await tx_response.getReceipt(client)
    topic_id = receipt.topicId
    await client.close()
    return str(topic_id)

async def submit_audit_log_async(topic_id: str, message: str):
    """Submits a message to a specific HCS topic."""
    if not client:
        raise Exception("Hedera client is not initialized. Check environment variables.")

    await TopicMessageSubmitTransaction(
        topicId=topic_id,
        message=bytes(message, 'utf-8')
    ).execute(client)
    await client.close()

# Synchronous wrappers for Flask
def create_audit_topic():
    return asyncio.run(create_audit_topic_async())

def submit_audit_log(topic_id: str, message: str):
    return asyncio.run(submit_audit_log_async(topic_id, message))


