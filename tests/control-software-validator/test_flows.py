import zmq
from models.publish_state_message import PublishStateMessage
from zmq.asyncio import Context

context = Context()


async def test_publish_state():
    stream = context.socket(zmq.SUB)
    stream.connect("tcp://localhost:4204")
    stream.subscribe("")
    message = await stream.recv_string()
    parsed = PublishStateMessage.model_validate_json(message)
