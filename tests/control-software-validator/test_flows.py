import os
import uuid

import pytest
import zmq
from channels.request_channel import MockRequestChannel, RequestChannel
from channels.subscribe_channel import MockSubscribeChannel, SubscribeChannel
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
from zmq.asyncio import Context

# Settings
sub_address: str = os.environ.get("CSV_HWCS_SUB_ADDRESS", "tcp://localhost:4204")
req_address: str = os.environ.get("CSV_HWCS_REQ_ADDRESS", "tcp://localhost:4203")
mode: str = os.environ.get("CSV_MODE", "connect")

context: Context = Context()
version: str = "0.1.0"


@pytest.fixture
def req_channel() -> RequestChannel:
    req_stream = context.socket(zmq.REQ)
    if mode == "dry_run":
        return MockRequestChannel(req_stream)
    else:
        channel = RequestChannel(req_stream)
        channel.connect(req_address)
        return channel


@pytest.fixture
def sub_channel() -> SubscribeChannel:
    sub_stream = context.socket(zmq.SUB)
    if mode == "dry_run":
        return MockSubscribeChannel(sub_stream)
    else:
        channel = SubscribeChannel(sub_stream)
        channel.connect(sub_address)
        return channel


@pytest.mark.timeout(10)
async def test_publish_state(sub_channel: SubscribeChannel) -> None:
    # Test if published state message is correctly formatted
    _ = await sub_channel.receive(PublishStateMessage)


@pytest.mark.timeout(20)
async def test_static_data_request(req_channel: RequestChannel) -> None:
    # Test if static data reply is correctly formatted
    static_data_request = GetStaticRequest(version=version, command="get_static")
    await req_channel.request(static_data_request, GetStaticReplySuccess)


@pytest.mark.timeout(20)
async def test_dynamic_data_request(req_channel: RequestChannel) -> None:
    # Test if dynamic data reply is correctly formatted
    dynamic_data_request = GetDynamicRequest(version=version, command="get_dynamic")
    await req_channel.request(dynamic_data_request, GetDynamicReplySuccess)


@pytest.mark.timeout(120)
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


@pytest.mark.timeout(120)
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
