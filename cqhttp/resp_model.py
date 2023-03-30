from typing import Optional

from pydantic import BaseModel


class SendPrivateMsgResp(BaseModel):
    message_id: int

