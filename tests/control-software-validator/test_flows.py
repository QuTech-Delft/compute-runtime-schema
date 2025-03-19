import os
import uuid

import pytest
import zmq
from models.execute_reply_success import ExecuteReplySuccess
from models.execute_request import ExecuteRequest, QuantumHardwareRunCircuitPayload
from models.initialize_reply_success import InitializeReplySuccess
from models.initialize_request import InitializeRequest
from models.publish_state_message import PublishStateMessage
from models.terminate_reply_success import TerminateReplySuccess
from models.terminate_request import TerminateRequest
from zmq.asyncio import Context, Socket

context: Context = Context()
sub_address: str = os.environ.get("HWCS_SUB_ADDRESS", "tcp://localhost:4204")
req_address: str = os.environ.get("HWCS_REQ_ADDRESS", "tcp://localhost:4203")
version: str = "0.1.0"


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


async def test_publish_state(sub_stream: Socket) -> None:
    # Test if published state message is correctly formatted
    message = await sub_stream.recv_string()
    _ = PublishStateMessage.model_validate_json(message)


async def test_happy_flow(req_stream: Socket):
    session_id = uuid.uuid4()

    init_request = InitializeRequest(
        version=version, session_id=session_id, command="initialize"
    )
    req_stream.send_string(init_request.model_dump_json())
    message = await req_stream.recv_string()

    _ = InitializeReplySuccess.model_validate_json(message)

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

    req_stream.send_string(exec_request.model_dump_json())
    message = await req_stream.recv_string()

    _ = ExecuteReplySuccess.model_validate_json(message)

    terminate_request = TerminateRequest(
        version=version, session_id=session_id, command="terminate"
    )
    req_stream.send_string(terminate_request.model_dump_json())
    message = await req_stream.recv_string()

    _ = TerminateReplySuccess.model_validate_json(message)
