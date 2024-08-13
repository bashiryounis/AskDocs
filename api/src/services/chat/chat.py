import redis
import uuid
import os
from typing import List, Dict, Tuple , Union
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Query
from src.utils.rag import conversational_rag_chain, rag_answer
from src.utils.utils import get_all_conversations
from src.core.db import get_collection, get_redis
from src.services.chat.schema import ChatMessage, ChatSession
from src.services.chat.crud_chat import ChatService
from src.core.celery_config import celery_app

router = APIRouter()


def get_chat_service() -> ChatService:
    """
    Dependency to get the ChatService
    """
    mongo_collection = get_collection("chat_sessions")
    redis_client = get_redis()
    return ChatService(mongo_collection, redis_client)


@router.delete("/clean_redis_db")
def clear_redis_db(service: ChatService = Depends(get_chat_service)):
    """Clear all data from Redis."""
    return service.clear_redis_db()


@router.post("/start")
def start_chat_session(user_id: str, service: ChatService = Depends(get_chat_service)):
    """Start a new chat session for a user."""
    session_id = str(uuid.uuid4())
    service.create_session(session_id, user_id)
    return {"session_id": session_id}


@router.get("/session/{user_id}/")
def get_user_session(user_id: str, service: ChatService = Depends(get_chat_service)) -> List[ChatSession]:
    """Retrieve chat history from Redis for a specific session."""
    return service.get_user_chat_sessions(user_id)


@router.get("/{user_id}/{session_id}/redis_history")
def fetch_chat_redis(session_id: str, user_id: str, service: ChatService = Depends(get_chat_service)) -> Union[ChatSession, None]:
    """Retrieve chat history from Redis for a specific session."""
    return service.fetch_chat_redis(user_id=user_id, session_id=session_id)


@router.post("/redis")
def store_chat_redis(session: ChatSession, service: ChatService = Depends(get_chat_service)):
    """Store chat session in Redis.."""
    return service.store_chat_redis(session)


@router.delete("/redis")
def delete_chat_redis(session_id: str, user_id: str, service: ChatService = Depends(get_chat_service)):
    """Delete chat session from Redis for a specific session."""
    return service.delete_chat_redis(user_id=user_id, session_id=session_id)


@router.get("/{user_id}/{session_id}/history_mongo/")
def fetch_chat_mongo(session_id: str, user_id: str, service: ChatService = Depends(get_chat_service)):
    """Retrieve chat session from Mongo for a specific session."""
    return service.fetch_chat_mongo(user_id=user_id, session_id=session_id)


@router.post("/mongo/")
def store_chat_mongo(chat_session: ChatSession, service: ChatService = Depends(get_chat_service)):
    """
    store chat session in Mongo 
    """
    return service.store_chat_mongo(chat_session=chat_session)


@router.patch("/mongo/")
def update_chat_mongo(session: ChatSession, service: ChatService = Depends(get_chat_service)) -> ChatSession:
    """update chat session from Mongo for a specific session."""
    return service.update_chat_mongo(session)


@router.delete("/mongo/")
def delete_chat_mongo(session_id: str, service: ChatService = Depends(get_chat_service)):
    """
    Delete chat session from Mongo for a specific session.
    """
    session_to_delete=service.delete_chat_mongo(session_id)
    if not session_to_delete:
        raise HTTPException(status_code=404, detail="Session not found")
    if "_id" in session_to_delete:
        session_to_delete["_id"] = str(session_to_delete["_id"])
    return session_to_delete


@router.post("/{session_id}/expire/")
def expire_session(session_id: str, user_id: str, service: ChatService = Depends(get_chat_service)):
    """
    Expire a chat session and move its data from Redis to MongoDB.
    """
    service.expire_session(session_id, user_id)
    return {"detail": "Session expired and chat history stored in MongoDB"}


@router.post("/question_aware_history")
def chat_with_memory(
    qusetion: str = Form(..., description="please ask your question"),
    user_id: str = Form(..., description="please ask your question"),
    conversation_id: str = Form(..., description="please ask your question"),
):
    """
    Submit a question  and receive an answer base on conversation history and the RAG model. 
    """
    return conversational_rag_chain.invoke(
        {"input": qusetion},
        config={
            "configurable": {"user_id": user_id, "conversation_id": conversation_id}
        },
    )["answer"]


@router.post("/question")
def chat(
    question: str = Form(..., description="please ask your question")
):
    """
    Submit a question and receive an answer from the RAG model.
    """
    return rag_answer(question)


@router.get("/conversations-messages")
def get_conv(
    user_id: str = Query(..., description="please add your user id"),
    conversation_id: str = Query(...,
                                 description="please  add conversation id")
):
    """
    Retrieve all messages from a specific conversation.
    """
    return get_all_conversations(
        user_id=user_id,
        conversation_id=conversation_id
    )


@router.post("/move-chat-data/")
async def move_chat_data(user_id: str, session_id: str):
    """Endpoint to trigger the move_chat_data_to_mongo task."""
    result = celery_app.send_task(
        'src.services.chat.background_tasks.move_chat_data_to_mongo', args=[user_id, session_id])
    return {"task_id": result.id}


@router.post("/restore-chat-data/")
async def restore_chat_data(user_id: str, session_id: str):
    """Endpoint to trigger the restore_chat_data_to_redis task."""
    result = celery_app.send_task(
        'src.services.chat.background_tasks.restore_chat_data_to_redis', args=[user_id, session_id])
    return {"task_id": result.id}
