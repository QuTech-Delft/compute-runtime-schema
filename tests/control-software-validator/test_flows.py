import os
import uuid

import pytest
import zmq
from channels.request_channel import MockRequestChannel, RequestChannel
from channels.subscribe_channel import MockSubscribeChannel, SubscribeChannel
from models.v2_PublishState import V2PublishState
from models.v2_QuantumHardwareDynamicDataRequest import (
    V2QuantumHardwareDynamicDataRequest,
)
from models.v2_QuantumHardwareDynamicDataResponse import (
    V2QuantumHardwareDynamicDataResponse,
)
from models.v2_QuantumHardwareExecuteRequest import (
    RunCircuitPayloadSchema,
    V2QuantumHardwareExecuteRequest,
)
from models.v2_QuantumHardwareExecuteResponse import V2QuantumHardwareExecuteResponse
from models.v2_QuantumHardwareFailureResponse import V2QuantumHardwareFailureResponse
from models.v2_QuantumHardwareInitializeRequest import (
    V2QuantumHardwareInitializeRequest,
)
from models.v2_QuantumHardwareSimpleSuccessResponse import (
    V2QuantumHardwareSimpleSuccessResponse,
)
from models.v2_QuantumHardwareStaticDataRequest import (
    V2QuantumHardwareStaticDataRequest,
)
from models.v2_QuantumHardwareStaticDataResponse import (
    V2QuantumHardwareStaticDataResponse,
)
from models.v2_QuantumHardwareTerminateRequest import V2QuantumHardwareTerminateRequest
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
    _ = await sub_channel.receive(V2PublishState)


@pytest.mark.timeout(20)
async def test_static_data_request(req_channel: RequestChannel) -> None:
    # Test if static data reply is correctly formatted
    static_data_request = V2QuantumHardwareStaticDataRequest(
        version=version, command="get_static"
    )
    await req_channel.request(static_data_request, V2QuantumHardwareStaticDataResponse)


@pytest.mark.timeout(20)
async def test_dynamic_data_request(req_channel: RequestChannel) -> None:
    # Test if dynamic data reply is correctly formatted
    dynamic_data_request = V2QuantumHardwareDynamicDataRequest(
        version=version, command="get_dynamic"
    )
    await req_channel.request(
        dynamic_data_request, V2QuantumHardwareDynamicDataResponse
    )


@pytest.mark.timeout(120)
async def test_happy_flow(req_channel: RequestChannel):
    # Test normal init->execute->terminate flow
    session_id = uuid.uuid4()

    init_request = V2QuantumHardwareInitializeRequest(
        version=version, session_id=session_id, command="initialize"
    )
    await req_channel.request(init_request, V2QuantumHardwareSimpleSuccessResponse)

    exec_payload = RunCircuitPayloadSchema(
        job_id=1,
        circuit="version 1.0\nqubit[1] q\nbit[1] b\nX q[0]\nb[0] = measure q[0]",
        number_of_shots=10,
        include_raw_data=False,
    )
    exec_request = V2QuantumHardwareExecuteRequest(
        version=version,
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, V2QuantumHardwareExecuteResponse)

    terminate_request = V2QuantumHardwareTerminateRequest(
        version=version, session_id=session_id, command="terminate"
    )
    await req_channel.request(terminate_request, V2QuantumHardwareSimpleSuccessResponse)


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
    exec_request = V2QuantumHardwareExecuteRequest(
        version=version,
        session_id=session_id,
        command="execute",
        payload=exec_payload,
    )
    await req_channel.request(exec_request, V2QuantumHardwareFailureResponse)
