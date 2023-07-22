# Passive modus

In the passive mode, a broadcast model is followed. 2300 acts as a sender, while 2200 listens to the various messages.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Publish-subscribe. 2200 using SUB socket and 2300 PUB socket |
| Publish binding argument | `tcp://*:4204` i.e., uses underlying TCP socket connect to port 4204. |
| Subscriber connect argument | `tcp://<host address>:4204`. The `<host address>` contains the IP address of 2300. |

The messages are python dictionaries that are converted from/to python strings via the JSON serializer of the python standard library (`json.loads` and `json.dumps` functions).

The dictionaries, received by the subscribers, have the following structure:

| Key | Type | Value |
| --- | --- | --- |
| `command` | `str` | A string identifying the function to be executed. |
| `payload` | `dict` | Arguments for the function to be executed. Presence of this key-value pair depends on the specific command. |
| `version` | `str` | String containing the version number of the message format. This allows modification of the interface in a backwards compatible manner. The version will adhere to the [semantic versioning rules](<https://semver.org/>). Presently we are still using a beta numbering (`0.y.z`). |

## Application layer

The application layer contains the specific application functions that are described in the [root document](../index.md). The functions are described via the contents of the published dictionaries.

### Function to retrieve system information from 2300

System information from 2300 is divided over both active and passive communication. The messages below are published by 2300.

#### Publish status

The payload for the message is:

| Key | Type | Value |
| --- | --- | --- |
| `status` | `str` | The current status of the system in all-capitals (i.e. IDLE, EXECUTING, CALIBRATING, OFFLINE) |
| `timestamp` | `float` | Timestamp of the instantiation of the message (return value of `time.time()`) |

```json
{
    "session_id": "abcd",
    "command": "publish_status",
    "payload": {
        "status": "IDLE",
        "timestamp": 1690061619.610174
    },
    "version": "0.1.0"
}
```

#### Publish dynamic

The payload for the message is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "abcd",
    "command": "publish_dynamic",
    "payload": {},
    "version": "0.1.0"
}
```
