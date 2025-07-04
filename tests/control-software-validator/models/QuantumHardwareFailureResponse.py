# generated by datamodel-codegen:
#   filename:  QuantumHardwareFailureResponse.schema.json

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class FailureDataSchema(BaseModel):
    error_msg: str = Field(
        ...,
        description='A descriptive error message to be passed on to the user.',
        title='Error Msg',
    )


class QuantumHardwareFailureResponse(BaseModel):
    session_id: UUID = Field(
        ...,
        description='An arbitrary string, filled in in the request, which is copied into the reply object.',
        title='Session Id',
    )
    status: Literal['failure'] = Field(..., title='Status')
    payload: FailureDataSchema
