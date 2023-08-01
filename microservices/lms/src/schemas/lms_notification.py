"""
Pydantic Model for notification API's
"""
import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import INPUT_REPLAY_NOTIFICATION_EXAMPLE

class InputReplayNotificationModel(BaseModel):
    """Replay Notification Pydantic Model
    Args:
        BaseModel (_type_): _description_
    """
    start_date: datetime.datetime
    end_date: datetime.datetime
    class Config():
        "Pydantic Config Class"
        orm_mode = True
        schema_extra = {"example": INPUT_REPLAY_NOTIFICATION_EXAMPLE}


class ReplayNotificationResponseModel(BaseModel):
    """Replay Notification Model"""
    success: Optional[bool] = True
    message: Optional[str] = "Successfully published messages"
    data: Optional[str] = None

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully republished messages",
                "data": None
            }
        }