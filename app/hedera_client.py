import os
from hashgraph_sdk import (
    Client,
    PrivateKey,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction
)

# Configure the client for Hedera Testnet
try:
    operator_id = os.getenv("HEDERA_ACCOUNT_ID")
    operator_key_str = os.getenv("HEDERA_PRIVATE_KEY")

    if not operator_id or not operator_key_str:
        raise ValueError("HEDERA_ACCOUNT_ID and HEDERA_PRIVATE_KEY must be set in environment variables.")

    # The private key might have a '0x' prefix, which the SDK doesn't expect.
    if operator_key_str.startswith("0x"):
        operator_key_str = operator_key_str[2:]

    operator_key = PrivateKey.fromString(operator_key_str)

    client = Client.forTestnet()
    client.setOperator(operator_id, operator_key)
except Exception as e:
    # This will help debug if the environment variables are set incorrectly
    print(f"Error initializing Hedera client: {e}")
    client = None

async def create_audit_topic() -> str:
    """Creates a new HCS topic and returns the Topic ID as a string."""
    if not client:
        raise Exception("Hedera client is not initialized. Check environment variables.")

    tx_response = await TopicCreateTransaction().execute(client)
    receipt = await tx_response.getReceipt(client)
    topic_id = receipt.topicId
    return str(topic_id)

async def submit_audit_log(topic_id: str, message: str):
    """Submits a message to a specific HCS topic."""
    if not client:
        raise Exception("Hedera client is not initialized. Check environment variables.")

    await TopicMessageSubmitTransaction(
        topicId=topic_id,
        message=bytes(message, "utf-8")
    ).execute(client)


