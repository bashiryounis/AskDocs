from src.core.celery_config import celery_app
from src.services.chat.crud_chat import ChatService
from src.core.db import get_collection, get_redis
import logging

logger = logging.getLogger(__name__)

mongo_collection = get_collection("chat_sessions")
redis_client = get_redis()

chat_service = ChatService(mongo_collection, redis_client)


@celery_app.task
def move_chat_data_to_mongo(user_id, session_id):
    """Move chat data from Redis to MongoDB when session expires."""
    logger.info(f"Starting to move chat data for user_id={user_id}, session_id={session_id}")
    chat_data = chat_service.fetch_chat_redis(session_id=session_id, user_id=user_id)
    if chat_data:
        existing_chat_data = chat_service.fetch_chat_mongo(session_id=session_id, user_id=user_id)
        if existing_chat_data:
            chat_service.update_chat_mongo(chat_data)
            logger.info(f"Updated chat data in MongoDB for session_id={session_id}")
        else:
            chat_service.store_chat_mongo(chat_data)
            logger.info(f"Stored chat data in MongoDB for session_id={session_id}")

        chat_service.delete_chat_redis(session_id=session_id, user_id=user_id)
        logger.info(f"Deleted chat data from Redis for session_id={session_id}")
    else:
        logger.warning(f"No chat data found for user_id={user_id}, session_id={session_id}")


@celery_app.task
def restore_chat_data_to_redis(user_id: str, session_id: str):
    """Restore chat data from MongoDB to Redis when session is restored."""
    try:
        chat_data = chat_service.fetch_chat_mongo(session_id, user_id)
        if chat_data:
            chat_service.store_chat_redis(chat_data)
            logger.info(f"Successfully restored chat data for session ID: {session_id} and user ID: {user_id}")
        else:
            logger.warning(f"No chat data found for session ID: {session_id} and user ID: {user_id}")
    except Exception as e:
        logger.error(f"Error occurred while restoring chat data for session ID: {session_id} and user ID: {user_id}: {e}")
