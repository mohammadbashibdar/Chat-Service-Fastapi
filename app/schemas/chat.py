from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union, Dict
from app.schemas.enum import ChatMessageVoteType, ChatMessageType

class ChatRoomMemberInput(BaseModel):
    chatroom_id: int
    users: Optional[List[int]] = Field(default_factory=list)

class ChatRoomCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    read_only: Optional[bool] = False
    mute: Optional[bool] = False
    profile_image: Optional[str] = None


class ChatRoomOut(BaseModel):
    id: int
    building_id: int
    name: Optional[str]
    description: Optional[str]
    read_only: bool
    mute: bool
    is_private: bool
    profile_image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AddMemberOut(BaseModel):
    chatroom_id: int
    inserted_count: int
    total_members: int
    is_private: bool
    inserted: dict
    already_exists: dict

class DeleteChatroomContact(BaseModel):
    chatroom_id: int
    deleted_count: int


class ChatRoomMemberRemoveInput(BaseModel):
    chatroom_id: int
    users: Optional[List[int]] = Field(default_factory=list)

class CreateMessageInput(BaseModel):
    chat_room: int
    type: ChatMessageType
    content: Optional[str] = None
    like: Optional[List[int]] = Field(default_factory=list)
    dislike: Optional[List[int]] = Field(default_factory=list)
    files: Optional[List[str]] = Field(default_factory=list)
    private: Optional[bool] = False
    vote_type: Optional[ChatMessageVoteType] = None
    vote_is_anonymous: Optional[bool] = False
    vote_is_optional: Optional[bool] = False
    vote_expiry: Optional[datetime] = None
    vote_answers_visible_to: Optional[str] = None
    vote_options: Optional[List[str]] = Field(default_factory=list)
    vote_selected_options: Optional[List[str]] = Field(default_factory=list)

class ChatMessageOut(BaseModel):
    id: int
    type: str
    content: Optional[str]
    chat_room: int
    sender_id: int
    files: Optional[List[str]] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRoomResponse(BaseModel):
    id: int
    building_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    read_only: bool
    mute: bool
    is_private: bool
    profile_image: Optional[str] = None
    manager_ids: Optional[List[int]]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    name: Optional[str]
    profile_image: Optional[str]

    class Config:
        from_attributes = True

class ChatMessagesOut(BaseModel):
    id: int
    type: ChatMessageType
    content: Optional[str]
    like: bool
    dislike: bool
    chat_room: int
    sender: Optional[UserBase] = Field(alias="user_sender")
    is_deleted: bool
    is_edited: bool
    reply_to: Optional[int]
    forwarded_from: Optional[int]
    files: Optional[List[str]] = []
    private: bool
    like_count: int
    dislike_count: int
    vote_count: int
    vote_type: Optional[str]
    vote_is_anonymous: bool
    vote_is_optional: bool
    vote_expiry: Optional[datetime]
    vote_answers_visible_to: Optional[Any]
    vote_options: Optional[Any]
    vote_selected_options: Optional[Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ChatMessages(BaseModel):
    # room_id: int
    count: Optional[int]
    offset: Optional[int]

class ChatRoomInfoOut(BaseModel):
    id: int
    building_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    read_only: Optional[bool] = False
    mute: Optional[bool] = False
    is_private: Optional[bool] = False
    manager_ids: Optional[List[int]] = []
    profile_image: Optional[str] = None


    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: int
    type: Optional[str]
    content: Optional[str]
    like: bool
    dislike: bool
    chat_room: int
    sender_id: Optional[int]
    is_deleted: bool
    is_edited: bool
    reply_to: Optional[int]
    forwarded_from: Optional[int]
    files: Optional[List[str]] = []
    private: bool
    like_count: int
    dislike_count: int
    vote_count: int
    vote_type: Optional[str]
    vote_is_anonymous: bool
    vote_is_optional: bool
    vote_expiry: Optional[datetime]
    vote_answers_visible_to: Optional[Any]
    vote_options: Optional[Any]
    vote_selected_options: Optional[Any]

    class Config:
        from_attributes = True


class PrivateMessageCreate(BaseModel):
    user_id: int
    type: ChatMessageType
    content: Optional[str] = None
    like: Optional[bool] = False
    dislike: Optional[bool] = False
    is_deleted: Optional[bool] = False
    is_edited: Optional[bool] = False
    reply_to: Optional[int] = None
    forwarded_from: Optional[int] = None
    files: Optional[List[str]] = []
    vote_type: Optional[ChatMessageVoteType] = None
    vote_is_anonymous: Optional[bool] = False
    vote_is_optional: Optional[bool] = False
    vote_expiry: Optional[datetime] = None
    vote_answers_visible_to: Optional[Any] = None
    vote_options: Optional[Any] = None
    vote_selected_options: Optional[Any] = None


class ChatMessagePrivetOut(BaseModel):
    id: int
    chat_room: int
    sender_id: int
    type: ChatMessageType
    content: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class RemoveMemberOut(BaseModel):
    chatroom_id: int
    deleted_count: int
    not_found: Dict[str, List[Union[int, str]]]

    class Config:
        from_attributes = True