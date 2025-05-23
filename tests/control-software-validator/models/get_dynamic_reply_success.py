# generated by datamodel-codegen:
#   filename:  reply_success.schema.json

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class QuantumHardwareDynamicData(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class GetDynamicReplySuccess(BaseModel):
    version: str = Field(..., pattern='^\\d+\\.\\d+\\.\\d$', title='Version')
    status: Literal['success'] = Field(..., title='Status')
    payload: QuantumHardwareDynamicData = Field(
        ..., description='The return value(s) of the executed command.'
    )
