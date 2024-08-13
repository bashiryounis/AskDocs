from langchain_community.chat_message_histories import RedisChatMessageHistory

REDIS_URL = "redis://redis:6379"

def get_message_history(user_id: str, conversation_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=f"{user_id}:{conversation_id}", 
        key_prefix="message_store:",
        url=REDIS_URL)


def get_all_conversations(user_id: str, conversation_id: str) -> list:
    chat_history = get_message_history(user_id , conversation_id)
    conversation_output = []
    for message in chat_history.messages:
        conversation_output.append(f"{message.type}: {message.content}")
    return conversation_output