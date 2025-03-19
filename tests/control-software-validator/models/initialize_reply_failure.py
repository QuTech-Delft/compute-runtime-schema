# generated by datamodel-codegen:
#   filename:  reply_failure.schema.json
#   timestamp: 2025-03-19T13:34:52+00:00

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, constr


class QuantumHardwareFailureData(BaseModel):
    error_msg: str = Field(
        ...,
        description='A descriptive error message to be passed on to the user.',
        title='Error Msg',
    )


class InitializeReplyFailure(BaseModel):
    version: constr(pattern=r'^\d+\.\d+\.\d$') = Field(..., title='Version')
    session_id: UUID = Field(
        ...,
        description='An arbitrary string, filled in in the request, which is copied into the reply object.',
        title='Session Id',
    )
    status: Literal['failure'] = Field(..., title='Status')
    payload: QuantumHardwareFailureData
