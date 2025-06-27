# Meta communication

System information from 2300 is divided over both request/reply and publish/subscribe. The messages below are published
by 2300.

## Publish state

System 2300 publishes a state message to inform subscribers of its current state. This happens both via a heartbeat
("am I still responsive") and the state the system is in.

!!! info
    The schemas for validation inherit can be found in:

    * `/schemas/<version>/PublishState.schema.json`

### Publish state payload

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

### Publish state example

```json title="publish_state.json" linenums="1"
{
    "command": "publish_state",
    "payload": {
        "state": "IDLE",
        "timestamp": 1690061619.610174
    },
}
```
