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

from app.schemas.chat import ChatRoomCreate, ChatRoomMemberInput, ChatRoomMemberRemoveInput, CreateMessageInput, \
    ChatRoomResponse
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



async def remove_members_from_chat_room(db: AsyncSession, members: ChatRoomMemberRemoveInput):
    chatroom_id = members.chatroom_id
    deleted_count = 0
    not_found = {
        "users": [],
    }

    if members.users:
        stmt = select(ChatRoomMember.user_id).where(
            and_(
                ChatRoomMember.chat_room_id == chatroom_id,
                ChatRoomMember.user_id.in_(members.users)
            )
        )
        result = await db.execute(stmt)
        existing_user_ids = result.scalars().all()
        to_delete = set(existing_user_ids)
        to_check = set(members.users)
        not_found["users"] = list(to_check - to_delete)

        if to_delete:
            stmt = delete(ChatRoomMember).where(
                and_(
                    ChatRoomMember.chat_room_id == chatroom_id,
                    ChatRoomMember.user_id.in_(list(to_delete))
                )
            )
            res = await db.execute(stmt)
            deleted_count += res.rowcount or 0


    await db.commit()

    return {
        "chatroom_id": chatroom_id,
        "deleted_count": deleted_count,
        "not_found": not_found
    }

async def verify_user_membership(db: AsyncSession, data: CreateMessageInput, user_id: int):
    stmt = select(ChatRoomMember).where(ChatRoomMember.chat_room_id == data.chat_room,ChatRoomMember.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def verify_chatroom_is_not_read_only(db: AsyncSession, data: CreateMessageInput):
    stmt = select(ChatRoom).where(ChatRoom.id == data.chat_room)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_message(db: AsyncSession, message_data: CreateMessageInput, sender_id: int):
    new_message = ChatMessage(
        type=message_data.type,
        content=message_data.content,
        chat_room=message_data.chat_room,
        sender_id=sender_id,
        is_deleted=False,
        is_edited=False,
        forwarded_from=None,
        private=message_data.private,
        like_count=0,
        dislike_count=0,
        vote_count=0,
        vote_type=message_data.vote_type,
        vote_is_anonymous=message_data.vote_is_anonymous,
        vote_is_optional=message_data.vote_is_optional,
        vote_expiry=message_data.vote_expiry,
        vote_answers_visible_to=message_data.vote_answers_visible_to,
        vote_options=message_data.vote_options,
        vote_selected_options=message_data.vote_selected_options,
        files=json.dumps(message_data.files) if message_data.files else None,
    )

    db.add(new_message)
    await db.flush()
    await db.commit()
    await db.refresh(new_message)
    if new_message.files:
        new_message.files = json.loads(new_message.files)
    return new_message


async def get_user_chat_rooms(db: AsyncSession, current_user: User) -> List[ChatRoomResponse]:
    result = await db.execute(select(ChatRoom).join(ChatRoom.users)
        .options(selectinload(ChatRoom.buildings), selectinload(ChatRoom.users))
        .where(ChatRoom.is_deleted == False, User.id == current_user.id)
    )
    rooms = result.scalars().all()

    chat_room_responses = []
    for room in rooms:
        name = room.name
        profile_image = room.profile_image

        if room.is_private:
            other_users = [user for user in room.users if user.id != current_user.id]
            if other_users:
                other_user = other_users[0]
                name = other_user.name
                profile_image = other_user.profile_image

        chat_room_responses.append(
            ChatRoomResponse(
                id=room.id,
                building_id=current_user.building_id,
                name=name,
                description=room.description,
                read_only=room.read_only,
                mute=room.mute,
                is_private=room.is_private,
                profile_image=profile_image,
                manager_ids=room.manager_ids,
            )
        )

    return chat_room_responses
