from pymongo.collection import Collection
from redis import Redis
from typing import List, Optional
from datetime import datetime
from src.services.chat.schema import ChatSession, ChatMessage
import json
import redis


class ChatService:
    def __init__(self, mongo_collection: Collection, redis_client: Redis):
        """
        Initialize the ChatService with MongoDB and Redis connections.
        """
        self.mongo_collection = mongo_collection
        self.redis_client = redis_client

    def create_session(self, session_id: str, user_id: str):
        """
        Initialize a new chat session in Redis based on session id and user id
        """
        session_key = f"{user_id}:{session_id}"
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "active",
            "initial_message": "User initiated a chat session.",
        }

        try:
            if self.redis_client.exists(session_key):
                raise ValueError(
                    f"Session ID {session_id} already exists for user {user_id}.")
            self.redis_client.hset(session_key, mapping=session_data)
            self.redis_client.delete(f"message_store:{session_key}")

            return (
                f"Session {session_id} created successfully for user {user_id}.")
        except Exception as e:
            return (
                f"Error creating session {session_id} for user {user_id}: {e}")

    def fetch_chat_session_redis(self, session_id: str, user_id: str) -> Optional[ChatSession]:
        """
        Fetch the entire ChatSession data directly from Redis.
        """
        try:
            key = f"{user_id}:{session_id}"
            session_data = self.redis_client.hgetall(key)
            if session_data:
                session_dict = {k.decode('utf-8'): v.decode('utf-8')
                                for k, v in session_data.items()}
                chat_session = ChatSession(**session_dict)
                return chat_session
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def fetch_chat_history_redis(self, session_id: str, user_id: str):
        """
        Fetch the entire Chat history  for spacfic session object directly from Redis.
        """
        messages = self.redis_client.lrange(
            f"message_store:{user_id}:{session_id}", 0, -1)
        chat_history = []
        for msg in messages:
            try:
                decoded_msg = json.loads(msg.decode('utf-8'))
                chat_message = ChatMessage(**decoded_msg.get('data', {}))
                chat_history.append(chat_message)
            except json.JSONDecodeError as e:
                return (f"Error decoding JSON: {e}")
            except Exception as e:
                return (f"Unexpected error: {e}")
        return chat_history

    def fetch_chat_redis(self, session_id: str, user_id: str):
        """
        Fetch the entire ChatSession data directly from Redis.
        """
        chat_history = self.fetch_chat_history_redis(user_id=user_id,session_id=session_id)
        chat_session = self.fetch_chat_session_redis(user_id=user_id, session_id=session_id)
        if chat_session is not None: 
            chat_session.chat_history = chat_history
            return chat_session
        return None

    def store_chat_redis(self, session) -> str:
        """
        Store chat data in Redis.
        """
        # Convert chat history to a list of dictionaries
        chat_history_json = [message.to_refined_json()
                             for message in session.chat_history]

        message_store_key = f"message_store:{session.user_id}:{session.session_id}"
        session_key = f"{session.user_id}:{session.session_id}"
        metadata = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "status": session.status,
            "initial_message": session.initial_message}
        try:
            # Store chat history as a list
            # Ensure it's empty before pushing
            self.redis_client.delete(message_store_key)
            for message_json in chat_history_json:
                self.redis_client.rpush(message_store_key, message_json)

            # Store metadata as a hash
            self.redis_client.hset(session_key, mapping=metadata)

            return f"Session data for session_id {session.session_id} stored successfully."
        except redis.RedisError as e:
            return f"An error occurred while storing session data for session_id {session.session_id}: {str(e)}"

    def delete_chat_redis(self, session_id: str, user_id: str):
        """
        delete entire session from redis db
        """
        session_key = f"{user_id}:{session_id}"
        message_store_key = f"message_store:{session_key}"
        try:
            session_deleted = self.redis_client.delete(session_key)
            message_store_deleted = self.redis_client.delete(message_store_key)
            if session_deleted == 0 and message_store_deleted == 0:
                return f"No session metadata or messages found for session_id: {session_id}"

            return f"Removed session metadata and messages for session_id: {session_id}"

        except redis.RedisError as e:
            return f"An error occurred while deleting session {session_id}: {str(e)}"

    def fetch_chat_mongo(self, session_id: str, user_id: str):
        """
        Fetch chat session from MongoDB.
        """
        session = self.mongo_collection.find_one(
            {"user_id": user_id, "session_id": session_id})
        if session:
            created_at = session.get("created_at")
            updated_at = session.get("updated_at")
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at)
                except ValueError:
                    created_at = datetime.utcnow()
            if isinstance(updated_at, str):
                try:
                    updated_at = datetime.fromisoformat(updated_at)
                except ValueError:
                    updated_at = datetime.utcnow()

            # Convert fields to correct types
            chat_history = session.get("chat_history", [])
            if isinstance(chat_history, list):
                chat_history = [ChatMessage(**msg) for msg in chat_history]
            else:
                chat_history = []

            chat_session = ChatSession(
                session_id=session.get("session_id", ""),
                user_id=session.get("user_id", ""),
                chat_history=chat_history,
                created_at=created_at,
                updated_at=updated_at,
                status=session.get("status", "expired"),
                initial_message=session.get("initial_message", "")
            )
            return chat_session
        return None

    def store_chat_mongo(self, chat_session):
        """
        Store chat session in MongoDB.
        """
        try:
            self.mongo_collection.insert_one(chat_session.dict())
            return (f"Chat session {chat_session.session_id} stored successfully in MongoDB.")
        except Exception as e:
            return (f"Error storing chat session in MongoDB: {e}")

    def update_chat_mongo(self, session):
        chat_history = [message.to_dict() for message in session.chat_history]
        update_fields = {
            "chat_history": chat_history,
            "metadata.updated_at": datetime.utcnow().isoformat()
        }
        result = self.mongo_collection.update_one(
            {"session_id": session.session_id},
            {"$set": update_fields})
        if result.matched_count > 0:
            updated_session = self.mongo_collection.find_one(
                {"session_id": session.session_id})
            return updated_session
        else:
            return (f"Session {session.session_id} not found. No update performed.")

    def delete_chat_mongo(self, session_id: str):
        return self.mongo_collection.find_one_and_delete({"session_id": session_id})

    def get_chat_history(self, session_id: str, user_id: str) -> List[ChatMessage]:
        """
        Retrieve chat history from Redis.
        """
        messages = self.redis_client.lrange(
            f"message_store:{user_id}:{session_id}", 0, -1)
        chat_history = []
        for msg in messages:
            try:
                decoded_msg = json.loads(msg.decode('utf-8'))
                chat_message = ChatMessage(
                    content=decoded_msg.get('data', {}).get('content'),
                    type=decoded_msg.get('data', {}).get("type"),
                    additional_kwargs=decoded_msg.get(
                        'data', {}).get('additional_kwargs'),
                    response_metadata=decoded_msg.get(
                        'data', {}).get('response_metadata'),
                    name=decoded_msg.get('data', {}).get('name'),
                    id=decoded_msg.get('data', {}).get('id'),
                    example=decoded_msg.get('data', {}).get('example'),
                    tool_calls=decoded_msg.get('data', {}).get('tool_calls'),
                    invalid_tool_calls=decoded_msg.get(
                        'data', {}).get('invalid_tool_calls'),
                    usage_metadata=decoded_msg.get(
                        'data', {}).get('usage_metadata'),
                )

                # Add the parsed ChatMessage to the chat history list
                chat_history.append(chat_message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        return chat_history

    def get_user_chat_sessions(self, user_id: str) -> List[ChatSession]:
        """
        Retrieve all chat sessions for a specific user from Redis and MongoDB.
        """
        sessions = []
        try:
            keys = self.redis_client.keys(f"{user_id}:*")
            for key in keys:
                key = key.decode("utf-8")
                if key.endswith(":messages"):
                    continue  # Skip message lists
                session_data = self.redis_client.hgetall(key)
                if not session_data:
                    continue  # Skip if session data is empty

                session_id = session_data.get(
                    b"session_id", b"").decode("utf-8")
                created_at = session_data.get(
                    b"created_at", b"").decode("utf-8")
                updated_at = session_data.get(b"updated_at", b"").decode(
                    "utf-8") if b"updated_at" in session_data else None
                status = session_data.get(b"status", b"").decode(
                    "utf-8") if b"status" in session_data else None

                # Retrieve chat history for the session
                chat_history = self.get_chat_history(session_id, user_id)
                session = (ChatSession(
                    session_id=session_id,
                    user_id=user_id,
                    chat_history=chat_history,
                    created_at=datetime.fromisoformat(
                        created_at) if created_at else None,
                    updated_at=datetime.fromisoformat(
                        updated_at) if updated_at else None,
                    status=status,
                    initial_message=session_data.get(
                        b"initial_message", b"").decode("utf-8"),
                ))
                sessions.append(session)
        except Exception as e:
            print(f"Error retrieving sessions from Redis: {e}")

        # # Retrieve expired sessions from MongoDB
        try:
            expired_sessions = self.mongo_collection.find({"user_id": user_id})
            for session in expired_sessions:
                # Retrieve and process created_at and updated_at
                created_at = session.get("created_at")
                updated_at = session.get(
                    "updated_at", datetime.utcnow().isoformat())

                if isinstance(created_at, str):
                    try:
                        created_at = datetime.fromisoformat(created_at)
                    except ValueError:
                        print(f"Error parsing created_at: {created_at}")
                        created_at = datetime.utcnow()  # Default value or handle as needed
                elif isinstance(created_at, datetime):
                    created_at = created_at.replace(
                        tzinfo=None)  # Ensure no timezone info

                if isinstance(updated_at, str):
                    try:
                        updated_at = datetime.fromisoformat(updated_at)
                    except ValueError:
                        print(f"Error parsing updated_at: {updated_at}")
                        updated_at = datetime.utcnow()  
                elif isinstance(updated_at, datetime):
                    updated_at = updated_at.replace(
                        tzinfo=None)  

                chat_session = ChatSession(
                    session_id=session.get("session_id", ""),
                    user_id=session.get("user_id", ""),
                    chat_history=[ChatMessage(
                        **msg) for msg in session.get("chat_history", [])],
                    created_at=created_at,
                    updated_at=updated_at,
                    status=session.get("status", "expired"),
                    initial_message=session.get("initial_message", "")
                )
                sessions.append(chat_session)
        except Exception as e:
            return(f"Error retrieving sessions from MongoDB: {e}")

        return sessions

    def clear_redis_db(self):
        """
        Clear all data from the Redis database.
        """
        try:
            self.redis_client.flushdb()
            return ("Redis database cleared successfully.")
        except Exception as e:
            return (f"Error clearing Redis database: {e}")
