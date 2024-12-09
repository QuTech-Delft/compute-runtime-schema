# Publish/Subscribe

For publish/subscribe, a broadcast model is followed. 2300 acts as a sender, while 2200 listens to the various messages.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Publish-subscribe. 2200 using SUB socket and 2300 PUB socket |
| Publish binding argument | `tcp://*:4204` i.e., uses underlying TCP socket connect to port 4204. |
| Subscriber connect argument | `tcp://<host address>:4204`. The `<host address>` contains the IP address of 2300. |

The messages in this section inherit from generic messages described in the [messages spec](../messages.md). Since
messages will only be broadcasted, only the [base request](../messages.md#base-request) will be used. Any new messages
should also inherit from this message.

## Application layer

The application layer contains the specific application functions that are described in the
[root document](../index.md). The functions are described via the contents of the published dictionaries.

### Meta communication

System information from 2300 is divided over both request/reply and publish/subscribe. The messages below are published
by 2300.

#### Publish state

System 2300 publishes a state message to inform subscribers of its current state. This happens both via a heartbeat
("am I still responsive") and the state the system is in.

The schemas for validation inherit from the **base schema** and can be found in:

* [`/schemas/publish_state/message.schema.json`](../../schemas/publish_state/message.schema.json)

##### Publish state payload

| Key | Type | Value |
| --- | --- | --- |
| `state` | `str` | The current state of the system in all-capitals (i.e. `IDLE`, `EXECUTING`, `CALIBRATING`, `OFFLINE`) |
| `timestamp` | `float` | Timestamp of the instantiation of the message (return value of `time.time()`) |

The various states are defined as described below. The first state that applies from top to bottom, is used in the
published message.

* `OFFLINE`: 2300 is controlled manually or not reachable,
* `CALIBRATING`: 2300 is calibrating,
* `EXECUTING`: 2300 is initialized for execution and not yet terminated,
* `IDLE`: 2300 is not executing experiments and being calibrated.

##### Publish state example

```jsonc
{
    "command": "publish_state",
    "payload": {
        "state": "IDLE",
        "timestamp": 1690061619.610174
    },
    "version": "0.2.0"
}
```
