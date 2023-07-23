# Active modus

In the active modus, the interface will be a client-server interface, with 2200 the client and 2300 the server. It follows the semantics of remote procedure calls (RPCs), i.e., the client "calls" a function that is "remotely" executed on the server and the result is passed back to the client.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Request-reply. 2200 using REQ socket and 2300 REP socket |
| Server binding argument | `tcp://*:4203` i.e., uses underlying TCP socket connect to port 4203. |
| Client connect argument | `tcp://<host address>:4203`. The `<host address>` contains the IP address of 2300. |

The messages are python dictionaries that are converted from/to python strings via the JSON serializer of the python standard library (`json.loads` and `json.dumps` functions).

The message used are described in the [messages spec](../messages.md). Both the base and extended messages are used.

## Application layer

The application layer contains the specific application functions that are described in the [root document](../index.md). The functions are described via the contents of the response and reply dictionaries.

### Function to avoid 2300 interrupting an algorithm from 2200

This function consists of two RPCs. One to start disabling of algorithm interruption and one to enable it again.

#### Initialize

This message signals to the 2300 that execution is about to begin. This initialize should be picked up as a request for locking 2300. However, this interpretation is left to this component.

The `payload` for the request is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "initialize",
    "version": "0.1.0"
}
```

The `payload` for the response is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

#### Terminate

The opposing message for the initialize request. When 2300 receives this request, execution from user generated circuits has stopped and the system can resume normal operations.

The `payload` for the request is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "terminate",
    "version": "0.1.0"
}
```

The `payload` for the response is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

### Function to execute algorithm

Execute an algorithm on 2300. This is only allowed when 2300 is in non-interruption mode. So for a single execution three commands are required, "initialize", "execute", "terminate".

#### Execute

This message requests a backend to execute a user generated circuit. This can only be done when the system has been initialized (in reality "locked").

The `payload` for the request is:

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `circuit` | `str` | Circuit description in cQASM language, see below for more information. |
| `number_of_shots` | `int` | Number of shots to be executed for the circuit. |

The cQASM language is described in detail [here](https://www.quantum-inspire.com/kbase/cqasm/). 2300 imposes the following constraints on the cQASM it accepts:

* The gates should be part of the allowed gates set.
* The requested number of qubits must be smaller or equal than the allowed number of qubits.
* Static loops are not allowed

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "execute",
    "payload": {
        "run_id": 1,
        "circuit": "version 1.0\n\nqubits 2",
        "number_of_shots": 1024
    },
    "version": "0.1.0"
}
```

The `payload` for the response is:

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `results` | `dict[str, int]` | Mapping of measured bitstring (little endian notation; `q[n]...q[0]`) to count of occurrences. |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "payload": {
        "run_id": 1,
        "results": {
            "000": 512,
            "001": 512
        }
    },
    "version": "0.1.0"
}
```

### Function to retrieve system information from 2300

System information from 2300 is divided over both active and passive communication. The messages below are triggered by 2200.

#### Get static

The `payload` for the request is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "get_static",
    "version": "0.1.0"
}
```

The `payload` for the response is:

| Key | Type | Value |
| --- | --- | --- |
| `nqubits` | `int` | The number of qubits |
| `topology` | `list[tuple]` | List of the edges between the various qubits |
| `name` | `str` | Name of the system |
| `pgs` | `list[str]` | Supported primitive gates set of the system. Gate names as described in cQASM (in uppercase). |
| `starttime` | `float` | Timestamp of start-up of the system (return value of `time.time()`) |

```json title="get_static_response.json"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "payload": {
        "nqubits": 5,
        "topology": [
            [0, 2],
            [1, 2],
            [3, 2],
            [4, 2]
        ],
        "name": "Starmon-5",
        "pgs": [
            "X",
            "Y"
        ],
        "starttime": 1690061619.610174
    },
    "version": "0.1.0"
}
```

#### Set publish

The `payload` for the request is:

| Key | Type | Value |
| --- | --- | --- |
| `active` | `bool` | Turn the PUB/SUB channel on, so that it starts broadcasting. This is a governance safeguard that initial messages are not missed and metadata on results is outdated. |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "set_publish",
    "payload": {
        "active": true
    },
    "version": "0.1.0"
}
```

The `payload` for the response is:

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

```json
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```
