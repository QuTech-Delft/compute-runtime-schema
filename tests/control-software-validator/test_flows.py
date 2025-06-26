import os
import uuid

import pytest
import zmq
from channels.request_channel import MockRequestChannel, RequestChannel
from channels.subscribe_channel import MockSubscribeChannel, SubscribeChannel
from models.PublishState import PublishState
from models.QuantumHardwareDynamicDataRequest import (
    QuantumHardwareDynamicDataRequest,
)
from models.QuantumHardwareDynamicDataResponse import (
    QuantumHardwareDynamicDataResponse,
)
from models.QuantumHardwareExecuteRequest import (
    QuantumHardwareExecuteRequest,
    RunCircuitPayloadSchema,
)
from models.QuantumHardwareExecuteResponse import QuantumHardwareExecuteResponse
from models.QuantumHardwareFailureResponse import QuantumHardwareFailureResponse
from models.QuantumHardwareInitializeRequest import (
    QuantumHardwareInitializeRequest,
)
from models.QuantumHardwareSimpleSuccessResponse import (
    QuantumHardwareSimpleSuccessResponse,
)
from models.QuantumHardwareStaticDataRequest import (
    QuantumHardwareStaticDataRequest,
)
from models.QuantumHardwareStaticDataResponse import (
    QuantumHardwareStaticDataResponse,
)
from models.QuantumHardwareTerminateRequest import QuantumHardwareTerminateRequest
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
    _ = await sub_channel.receive(PublishState)


@pytest.mark.timeout(20)
async def test_static_data_request(req_channel: RequestChannel) -> None:
    # Test if static data reply is correctly formatted
    static_data_request = QuantumHardwareStaticDataRequest(
        command="get_static", session_id=uuid.uuid4()
    )
    await req_channel.request(static_data_request, QuantumHardwareStaticDataResponse)


@pytest.mark.timeout(20)
async def test_dynamic_data_request(req_channel: RequestChannel) -> None:
    # Test if dynamic data reply is correctly formatted
    dynamic_data_request = QuantumHardwareDynamicDataRequest(
        command="get_dynamic", session_id=uuid.uuid4()
    )
    await req_channel.request(dynamic_data_request, QuantumHardwareDynamicDataResponse)


@pytest.mark.timeout(120)
async def test_happy_flow(req_channel: RequestChannel):
    # Test normal init->execute->terminate flow
    session_id = uuid.uuid4()

    init_request = QuantumHardwareInitializeRequest(
        session_id=session_id, command="initialize"
    )
    await req_channel.request(init_request, QuantumHardwareSimpleSuccessResponse)

    exec_payload = RunCircuitPayloadSchema(
        job_id=1,
        circuit="version 1.0\nqubit[1] q\nbit[1] b\nX q[0]\nb[0] = measure q[0]",
        number_of_shots=10,
        include_raw_data=False,
    )
    exec_request = QuantumHardwareExecuteRequest(
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, QuantumHardwareExecuteResponse)

    terminate_request = QuantumHardwareTerminateRequest(
        session_id=session_id, command="terminate"
    )
    await req_channel.request(terminate_request, QuantumHardwareSimpleSuccessResponse)


@pytest.mark.timeout(20)
async def test_exec_without_init(req_channel: RequestChannel):
    # Test if execute request without init request returns error
    session_id = uuid.uuid4()

    exec_payload = RunCircuitPayloadSchema(
        job_id=1,
        circuit="version 1.0\nqubit[1] q\nbit[1] b\nX q[0]\nb[0] = measure q[0]",
        number_of_shots=10,
        include_raw_data=False,
    )
    exec_request = QuantumHardwareExecuteRequest(
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, QuantumHardwareFailureResponse)
