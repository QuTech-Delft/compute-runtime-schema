# generated by datamodel-codegen:
#   filename:  QuantumHardwareExecuteRequest.schema.json

from __future__ import annotations

from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RunCircuitPayloadSchema(BaseModel):
    job_id: int = Field(
        ..., description='Client identifier for the execution', title='Job Id'
    )
    circuit: str = Field(
        ..., description='Circuit description in cQASM language', title='Circuit'
    )
    number_of_shots: int = Field(
        ...,
        description='Number of shots to be executed for the circuit.',
        gt=0,
        title='Number Of Shots',
    )
    include_raw_data: Optional[bool] = Field(
        False,
        description='Whether or not to return all bitstrings in the order in which they were measured.',
        title='Include Raw Data',
    )


class QuantumHardwareExecuteRequest(BaseModel):
    session_id: UUID = Field(
        ...,
        description='An arbitrary string, filled in in the request, which is copied into the reply object.',
        title='Session Id',
    )
    command: Literal['execute'] = Field(..., title='Command')
    payload: RunCircuitPayloadSchema
