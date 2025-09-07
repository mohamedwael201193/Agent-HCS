import os
from dotenv import load_dotenv
from hedera import (
    Client,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction,
    PrivateKey,
    AccountId
)

load_dotenv()

HEDERA_ACCOUNT_ID = os.getenv("HEDERA_ACCOUNT_ID")
HEDERA_PRIVATE_KEY = os.getenv("HEDERA_PRIVATE_KEY")

client = Client.forTestnet()
client.setOperator(AccountId.fromString(HEDERA_ACCOUNT_ID), PrivateKey.fromString(HEDERA_PRIVATE_KEY))

async def create_audit_topic():
    try:
        transaction_response = await TopicCreateTransaction().execute(client)
        receipt = await transaction_response.getReceipt(client)
        topic_id = receipt.topicId
        print(f"Topic created with ID: {topic_id}")
        return str(topic_id)
    except Exception as e:
        print(f"Error creating topic: {e}")
        return None

async def submit_audit_log(topic_id: str, message: str):
    try:
        transaction_response = await TopicMessageSubmitTransaction()
        .setTopicId(topic_id)
        .setMessage(message.encode(\'utf-8\'))
        .execute(client)
        receipt = await transaction_response.getReceipt(client)
        print(f"Message submitted to topic {topic_id}. Status: {receipt.status}")
        return True
    except Exception as e:
        print(f"Error submitting message: {e}")
        return False


