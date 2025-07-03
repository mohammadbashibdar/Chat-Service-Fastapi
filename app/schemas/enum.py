from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class ContactNumberType(str, Enum):
    mobile = "mobile"
    local = "local"
    phone = "phone"


class RuleType(str, Enum):
    text = "text"
    file = "file"


class NotificationMethons(str, Enum):
    SMS = "sms"
    PUSH = "push_notification"


class UnitUserFamilyType(str, Enum):
    SPOUSE = "SPOUSE"
    DAUGHTER = "DAUGHTER"
    SON = "SON"
    MOTHER = "MOTHER"
    FATHER = "FATHER"

class DaysOfWeek(str, Enum):
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"

class ChatMessageType(str, Enum):
    TEXT = "TEXT"
    FILE = "FILE"
    POLL = "POLL"
    NOTICE = "NOTICE"
    REACTION = "REACTION"
    VOTE_REPLY = "VOTE_REPLY"


class ChatMessageVoteType(str, Enum):
    LIKE_DISLIKE = "LIKE_DISLIKE"
    OPTION = "OPTION"
    DESCRIPTIVE = "DESCRIPTIVE"

class SessionType(str, Enum):
    GROUP = "group"
    ROLE = "role"
