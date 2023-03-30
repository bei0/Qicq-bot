from pydantic import BaseModel
from typing import Optional, List


class SendPrivateMsgRequest(BaseModel):
    user_id: int
    group_id: Optional[int]
    message: str
    auto_escape: bool = False


class SendGroupMsgRequest(BaseModel):
    group_id: int
    message: str
    auto_escape: bool = False
