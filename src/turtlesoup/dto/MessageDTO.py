from pydantic import BaseModel, Field

class CreateMessageDTO(BaseModel):
    content: str = Field(min_length=1)
    conversation_id: str = Field(min_length=1)


