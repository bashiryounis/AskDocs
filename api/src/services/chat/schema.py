from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Literal, Any
from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field
import json

class ChatMessage(BaseModel):
    content: Optional[str] = None
    type: Optional[str] = None
    additional_kwargs: Optional[Dict[str, Union[str, int, float, bool, None]]] = None
    response_metadata: Optional[Dict[str, Union[str, int, float, bool, None]]] = None
    name: Optional[Union[str, None]] = None
    id: Optional[Union[str, None]] = None
    example: Optional[bool] = None
    tool_calls: Optional[List[Dict[str, Union[str, int, float, bool, None]]]] = None
    invalid_tool_calls: Optional[List[Dict[str, Union[str, int, float, bool, None]]]] = None
    usage_metadata: Optional[Union[Dict[str, Union[str, int, float, bool, None]], None]] = None
    def to_refined_dict(self) -> dict:
        return {
            "type": self.type,
            "data": {
                "content": self.content,
                "additional_kwargs": self.additional_kwargs,
                "response_metadata": self.response_metadata,
                "name": self.name,
                "id": self.id,
                "example": self.example,
                "tool_calls": self.tool_calls,
                "invalid_tool_calls": self.invalid_tool_calls,
                "usage_metadata": self.usage_metadata
            }
        }

    def to_refined_json(self) -> str:
        return json.dumps(self.to_refined_dict())
    
    def to_dict(self) -> dict:
        # Create a dictionary representation of the ChatMessage instance
        return {
            "content": self.content,
            "type": self.type,
            "additional_kwargs": self.additional_kwargs,
            "response_metadata": self.response_metadata,
            "name": self.name,
            "id": self.id,
            "example": self.example,
            "tool_calls": self.tool_calls,
            "invalid_tool_calls": self.invalid_tool_calls,
            "usage_metadata": self.usage_metadata
        }
    


class ChatSession(BaseModel):
    session_id: str
    user_id: str
    chat_history: Optional[List[ChatMessage]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime
    status: str
    initial_message: Optional[str] = None
