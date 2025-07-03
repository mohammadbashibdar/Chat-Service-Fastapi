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
