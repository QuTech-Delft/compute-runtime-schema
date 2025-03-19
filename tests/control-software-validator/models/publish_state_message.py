# generated by datamodel-codegen:
#   filename:  message.schema.json

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, constr


class HWCSState(Enum):
    IDLE = 'IDLE'
    EXECUTING = 'EXECUTING'
    CALIBRATING = 'CALIBRATING'
    OFFLINE = 'OFFLINE'


class PublishStatePayload(BaseModel):
    timestamp: float = Field(
        ...,
        description='Timestamp of the instantiation of the message (return value of time.time())',
        title='Timestamp',
    )
    state: HWCSState


class PublishStateMessage(BaseModel):
    version: constr(pattern=r'^\d+\.\d+\.\d$') = Field(..., title='Version')
    command: Literal['publish_state'] = Field(..., title='Command')
    payload: PublishStatePayload = Field(
        ..., description='The return value(s) of the executed command.'
    )
