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

from app.schemas.chat import ChatRoomCreate, ChatRoomMemberInput
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


async def get_chatroom_by_id(db: AsyncSession, chatroom_id: int):
    result = await db.execute(select(ChatRoom).where(ChatRoom.id == chatroom_id))
    return result.scalars().first()


async def check_exist_input_param_add_user(db: AsyncSession, data: ChatRoomMemberInput) -> dict:
    try:
        not_found = {
            "users": [],

        }
        if data.users:
            for user_id in data.users:
                result = await db.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()
                if not user:
                    not_found["users"].append(user_id)


        return not_found

    except SQLAlchemyError:
        traceback.print_exc()
        return {
            "users": [],
            "error": "db"
        }


async def add_members_to_chat_room(db: AsyncSession, members: ChatRoomMemberInput):
    now = datetime.utcnow()
    chatroom_id = members.chatroom_id
    inserted_count = 0

    result = await db.execute(select(ChatRoomMember).where(ChatRoomMember.chat_room_id == chatroom_id))
    existing_members = result.scalars().all()

    existing_users = {m.user_id for m in existing_members if m.user_id is not None}

    already_exists = {
        "users": [],
    }
    inserted = {
        "users": [],
    }

    if members.users:
        new_users = []
        for user_id in members.users:
            if user_id in existing_users:
                already_exists["users"].append(user_id)
            else:
                new_users.append({"chat_room_id": chatroom_id, "user_id": user_id, "created_at": now})
                inserted["users"].append(user_id)
        if new_users:
            await db.execute(insert(ChatRoomMember).values(new_users))
            inserted_count += len(new_users)


    total_members = (
        len(set(inserted["users"]))
    )

    is_private = len(set(inserted["users"])) == total_members and total_members == 2

    await db.execute(update(ChatRoom).where(ChatRoom.id == chatroom_id).values(is_private=is_private))
    await db.commit()

    return {
        "chatroom_id": chatroom_id,
        "inserted_count": inserted_count,
        "total_members": total_members,
        "is_private": is_private,
        "inserted": inserted,
        "already_exists": already_exists
    }
