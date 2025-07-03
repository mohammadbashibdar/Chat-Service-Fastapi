from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.chat import ChatRoomCreate, ChatRoomOut, ChatRoomMemberInput, AddMemberOut, ChatRoomMemberRemoveInput, \
    CreateMessageInput, ChatMessageOut, ChatRoomResponse, ChatMessages, ChatMessagesOut, ChatRoomInfoOut, MessageOut, \
    PrivateMessageCreate, ChatMessagePrivetOut, RemoveMemberOut
from app.schemas.responses import SuccessResponse, ErrorResponse
from fastapi.responses import JSONResponse
import app.crud.chat as crud_chat
from app.schemas.user import SessionBase, UserSimple
from app.core.config import settings



async def create_chat_room(db: AsyncSession, data: ChatRoomCreate, current_user: User):
    exist_chat = await crud_chat.get_chatroom_by_name(db, data.name)
    if exist_chat:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="A chat room already exists with this name. It is not possible to create another one with this name.",
                code=404,
                errors=None
            ).dict()
        )
    check_input_param = await crud_chat.check_input_param_create_chat(data)
    if not check_input_param:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="The name value must be entered.",
                code=400,
                errors=None
            ).dict()
        )
    create = await crud_chat.create_chat_room(db, data, current_user.building_id)
    if not create:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Bad request.",
                code=400,
                errors=None
            ).dict()
        )
    return SuccessResponse(
        success=True,
        message="chat room created successfully.",
        data=ChatRoomOut.from_orm(create)
    )


async def addMember_to_chatroom(db: AsyncSession, data_add_member: ChatRoomMemberInput):
    exist_chatroom = await crud_chat.get_chatroom_by_id(db, data_add_member.chatroom_id)
    if not exist_chatroom:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Cannot add a member to the chat room. The entered chat room is not valid.",
                code=404,
                errors=None
            ).dict()
        )
    check_exist_input_param = await crud_chat.check_exist_input_param_add_user(db, data_add_member)
    errors = []
    if check_exist_input_param["users"]:
        errors.append(f"user by id {check_exist_input_param['users']} not found")

    if errors:
        return SuccessResponse(
            success=False,
            status_code=400,
            message="، ".join(errors)
        )

    added_member = await crud_chat.add_members_to_chat_room(db, data_add_member)
    if not added_member:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Bad request.",
                code=404,
                errors=None
            ).dict()
        )

    return SuccessResponse(
        success=True,
        message="added member to chatroom successfully",
        data=AddMemberOut(**added_member)
    )


async def remove_member_from_chatroom(data: ChatRoomMemberRemoveInput,db: AsyncSession):
    exist_chatroom = await crud_chat.get_chatroom_by_id(db, data.chatroom_id)
    if not exist_chatroom:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="The entered chat room is not valid.",
                code=404,
                errors=None
            ).dict()
        )

    result = await crud_chat.remove_members_from_chat_room(db, data)

    return SuccessResponse(
        success=True,
        message="Removed members from chatroom successfully",
        data=RemoveMemberOut(**result)
    )


async def send_message(db: AsyncSession, data: CreateMessageInput, sender_id: int):
    check_exist_user = await crud_chat.verify_user_membership(db, data, sender_id)
    if not check_exist_user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                success=False,
                message="User is not valid.",
                code=404,
                errors=None
            ).dict()
        )

    check_read_only = await crud_chat.verify_chatroom_is_not_read_only(db, data)
    if not check_read_only:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Chat room not found.",
                code=400,
                errors=None
            ).dict()
        )

    create_message = await crud_chat.create_message(db, data, sender_id)
    if not create_message:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Bad request.",
                code=400,
                errors=None
            ).dict()
        )

    return SuccessResponse(
        success=True,
        message="send message created successfully",
        data=ChatMessageOut.from_orm(create_message)
    )


async def get_all_chatRoom(db: AsyncSession, current_user: User):
    try:
        get_chatRoom_all = await crud_chat.get_user_chat_rooms(db, current_user)

        return SuccessResponse(
            success=True,
            message="get ChatRoom successfully",
            data=get_chatRoom_all
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Failed to fetch chatRoom",
                code=400,
                errors={"detail": str(e)}).dict()
        )


async def get_messages_service(db: AsyncSession, data: ChatMessages, room_id: int):
    try:
        get_message_in_chatRoom =  await crud_chat.get_messages_by_room_id(db, room_id, data)

        messages_out = [ChatMessagesOut.from_orm(msg) for msg in get_message_in_chatRoom]
        return SuccessResponse(
            success=True,
            message="get message successfully",
            data=messages_out
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                message="Failed to fetch Message",
                code=400,
                errors={"detail": str(e)}).dict()
        )
