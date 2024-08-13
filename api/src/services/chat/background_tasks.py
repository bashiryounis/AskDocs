from src.core.celery_config import celery_app
from src.services.chat.crud_chat import ChatService
from src.core.db import get_collection, get_redis


mongo_collection = get_collection("chat_sessions")
redis_client = get_redis()

chat_service = ChatService(mongo_collection, redis_client)


@celery_app.task
def move_chat_data_to_mongo(user_id, session_id):
    """Move chat data from Redis to MongoDB when session expires."""
    chat_data = chat_service.fetch_chat_redis(
        session_id=session_id, user_id=user_id)
    if chat_data:
        existing_chat_data = chat_service.fetch_chat_mongo(
            session_id=session_id, user_id=user_id)
        if existing_chat_data:
            chat_service.update_chat_mongo(chat_data)
        else:
            chat_service.store_chat_mongo(chat_data)
        chat_service.delete_chat_redis(session_id=session_id, user_id=user_id)
    else:
        print(
            f"No chat data found for user ID: {user_id}, session ID: {session_id}")


@celery_app.task
def restore_chat_data_to_redis(user_id, session_id):
    """Restore chat data from MongoDB to Redis when session is restored."""
    chat_data = chat_service.fetch_chat_mongo(session_id, user_id)
    if chat_data:
        chat_service.store_chat_redis(chat_data)
    else:
        print(f"No chat data found for session ID: {session_id}")
