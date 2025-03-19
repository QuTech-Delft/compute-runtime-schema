import os
import uuid
from typing import Any

import pytest
import zmq
from models.execute_reply_success import ExecuteReplySuccess
from models.execute_request import ExecuteRequest, QuantumHardwareRunCircuitPayload
from models.get_dynamic_reply_success import GetDynamicReplySuccess
from models.get_dynamic_request import GetDynamicRequest
from models.get_static_reply_success import GetStaticReplySuccess
from models.get_static_request import GetStaticRequest
from models.initialize_reply_success import InitializeReplySuccess
from models.initialize_request import InitializeRequest
from models.publish_state_message import PublishStateMessage
from models.terminate_reply_success import TerminateReplySuccess
from models.terminate_request import TerminateRequest
from pydantic import BaseModel
from zmq.asyncio import Context, Socket

context: Context = Context()
sub_address: str = os.environ.get("HWCS_SUB_ADDRESS", "tcp://localhost:4204")
req_address: str = os.environ.get("HWCS_REQ_ADDRESS", "tcp://localhost:4203")
version: str = "0.1.0"


class RequestChannel:
    def __init__(self, req_stream: Socket) -> None:
        self.req_stream = req_stream

    async def request(self, request: BaseModel, return_type: type[BaseModel]) -> Any:
        self.req_stream.send_string(request.model_dump_json())
        reply = await self.req_stream.recv_string()
        return return_type.model_validate_json(reply)


@pytest.fixture
def sub_stream() -> Socket:
    stream = context.socket(zmq.SUB)
    stream.connect(sub_address)
    stream.subscribe("")

    return stream


@pytest.fixture
def req_stream() -> Socket:
    stream = context.socket(zmq.REQ)
    stream.connect(req_address)

    return stream


@pytest.fixture
def req_channel(req_stream: Socket) -> RequestChannel:
    return RequestChannel(req_stream)


async def test_publish_state(sub_stream: Socket) -> None:
    # Test if published state message is correctly formatted
    message = await sub_stream.recv_string()
    _ = PublishStateMessage.model_validate_json(message)


async def test_static_data_request(req_channel: RequestChannel) -> None:
    # Test if static data reply is correctly formatted
    static_data_request = GetStaticRequest(version=version, command="get_static")
    await req_channel.request(static_data_request, GetStaticReplySuccess)


async def test_dynamic_data_request(req_channel: RequestChannel) -> None:
    # Test if dynamic data reply is correctly formatted
    dynamic_data_request = GetDynamicRequest(version=version, command="get_dynamic")
    await req_channel.request(dynamic_data_request, GetDynamicReplySuccess)


async def test_happy_flow(req_channel: RequestChannel):
    # Test normal init->execute->terminate flow
    session_id = uuid.uuid4()

    init_request = InitializeRequest(
        version=version, session_id=session_id, command="initialize"
    )
    await req_channel.request(init_request, InitializeReplySuccess)

    exec_payload = QuantumHardwareRunCircuitPayload(
        job_id=1,
        circuit="version 1.0\nqubit[1] q\nbit[1] b\nX q[0]\nb[0] = measure q[0]",
        number_of_shots=10,
        include_raw_data=False,
    )
    exec_request = ExecuteRequest(
        version=version,
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, ExecuteReplySuccess)

    terminate_request = TerminateRequest(
        version=version, session_id=session_id, command="terminate"
    )
    await req_channel.request(terminate_request, TerminateReplySuccess)


async def test_two_init_flow(req_channel: RequestChannel):
    # Control software should allow multiple initialize requests
    session_id = uuid.uuid4()

    init_request = InitializeRequest(
        version=version, session_id=session_id, command="initialize"
    )
    await req_channel.request(init_request, InitializeReplySuccess)

    exec_payload = QuantumHardwareRunCircuitPayload(
        job_id=1,
        circuit="version 1.0\nqubit[1] q\nbit[1] b\nX q[0]\nb[0] = measure q[0]",
        number_of_shots=10,
        include_raw_data=False,
    )
    exec_request = ExecuteRequest(
        version=version,
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, ExecuteReplySuccess)

    init_request = InitializeRequest(
        version=version, session_id=session_id, command="initialize"
    )
    await req_channel.request(init_request, InitializeReplySuccess)

    terminate_request = TerminateRequest(
        version=version, session_id=session_id, command="terminate"
    )
    await req_channel.request(terminate_request, TerminateReplySuccess)
