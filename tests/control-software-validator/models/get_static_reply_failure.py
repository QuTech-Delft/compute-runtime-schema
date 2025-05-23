# generated by datamodel-codegen:
#   filename:  reply_failure.schema.json

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GetStaticReplyFailure(BaseModel):
    version: str = Field(..., pattern='^\\d+\\.\\d+\\.\\d$', title='Version')
    status: Literal['failure'] = Field(..., title='Status')
