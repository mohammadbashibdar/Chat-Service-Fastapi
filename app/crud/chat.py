from app.models.chat_rooms import ChatRoom
from app.models.chat_messages import ChatMessage
from app.models.chat_room_members import ChatRoomMember
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, and_, func

from datetime import datetime
from typing import List
import traceback
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
import json

from app.schemas.chat import ChatRoomCreate
from app.schemas.enum import ChatMessageType

async def get_chatroom_by_name(db: AsyncSession, chat_name: str):
    result = await db.execute(select(ChatRoom).where(ChatRoom.name == chat_name))
    return result.scalars().first()

async def check_input_param_create_chat(data: ChatRoomCreate) -> bool:
    if data.name == None:
        return False
    return True

async def create_chat_room(db: AsyncSession, chat_data: ChatRoomCreate, building_id: int):
    is_private = True
    chat_room = ChatRoom(
        name=chat_data.name,
        description=chat_data.description,
        read_only=chat_data.read_only,
        mute=chat_data.mute,
        is_private=is_private,
        building_id=building_id,
        profile_image=chat_data.profile_image
    )
    db.add(chat_room)
    await db.commit()
    return chat_room

async def is_user_in_chatroom(db: AsyncSession, user_id: int, room_id: int) -> bool:
    query = select(ChatRoomMember).where(ChatRoomMember.chat_room_id == room_id, ChatRoomMember.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().first() is not None
