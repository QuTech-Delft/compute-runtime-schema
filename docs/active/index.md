# Active modus

In the active modus, the interface will be a client-server interface. 2200 acts as the client and 2300 as the server. It follows the semantics of remote procedure calls (RPCs), i.e., the client "calls" a function that is "remotely" executed on the server and the result is passed back to the client.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Request-reply. 2200 using REQ socket and 2300 REP socket |
| Server binding argument | `tcp://*:4203` i.e., uses underlying TCP socket connect to port 4203. |
| Client connect argument | `tcp://<host address>:4203`. The `<host address>` contains the IP address of 2300. |

The messages used are described in the [messages spec](../messages.md). Both the base and extended messages are used.

## Application layer

The application layer contains the specific application functions that are described in the [root document](../index.md). The functions are described via the contents of the response and reply dictionaries.

### Locking

This function consists of two RPCs. One to disable the algorithm interruption and one to enable it again.

#### Initialize

This message signals to the 2300 that execution is about to begin. The initialize should be picked up as a request for locking 2300. However, this interpretation is left to this component.

The schemas for validation can be found in:

* [`/schemas/initialize/request.schema.json`](../../schemas/initialize/request.schema.json)
* [`/schemas/initialize/response.schema.json`](../../schemas/initialize/response.schema.json)

##### Initialize request payload

This message does not require any additional information in the payload section.

##### Initialize request example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "initialize",
    "version": "0.1.0"
}
```

##### Initialize response payload

This message does not require any additional information in the payload section.

##### Initialize response example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

#### Terminate

The opposing message for the initialize request. When 2300 receives this request, execution from user generated circuits has stopped and the system can resume normal operations.

The schemas for validation can be found in:

* [`/schemas/terminate/request.schema.json`](../../schemas/terminate/request.schema.json)
* [`/schemas/terminate/response.schema.json`](../../schemas/terminate/response.schema.json)

##### Terminate request payload

This message does not require any additional information in the payload section.

##### Terminate request example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "terminate",
    "version": "0.1.0"
}
```

##### Terminate response payload

This message does not require any additional information in the payload section.

##### Terminate response example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

### Execution

Execute an algorithm on 2300. This is only allowed when 2300 is in non-interruption mode. So for a single execution three commands are required, "initialize", "execute", "terminate".

#### Execute

This message requests a backend to execute a user generated circuit. This can only be done when the system has been initialized (in reality "locked").

The schemas for validation can be found in:

* [`/schemas/execute/request.schema.json`](../../schemas/execute/request.schema.json)
* [`/schemas/execute/response.schema.json`](../../schemas/execute/response.schema.json)

##### Execute request payload

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `circuit` | `str` | Circuit description in cQASM language, see below for more information. |
| `number_of_shots` | `int` | Number of shots to be executed for the circuit. |

The cQASM language is described in detail [here](https://www.quantum-inspire.com/kbase/cqasm/). 2300 imposes the following constraints on the cQASM it accepts:

* The gates should be part of the allowed gates set.
* The requested number of qubits must be smaller or equal than the allowed number of qubits.
* Static loops are not allowed

##### Execute request example

```jsonc
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

##### Execute response payload

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `results` | `dict[str, int]` | Mapping of measured bitstring (little endian notation; `q[n]...q[0]`) to count of occurrences. |

##### Execute response example

```jsonc
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

### Meta communication

System information from 2300 is divided over both active and passive communication. The messages below are triggered by 2200.

#### Get static

Get system information from 2300. This information is retrieved only once, normally at startup time for 2200.

The schemas for validation can be found in:

* [`/schemas/get_static/request.schema.json`](../../schemas/get_statis/request.schema.json)
* [`/schemas/get_static/response.schema.json`](../../schemas/get_static/response.schema.json)

##### Get static request payload

This message does not require any additional information in the payload section.

##### Get static request example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "get_static",
    "version": "0.1.0"
}
```

##### Get static response payload

| Key | Type | Value |
| --- | --- | --- |
| `nqubits` | `int` | The number of qubits |
| `topology` | `list[tuple]` | List of the edges between the various qubits |
| `name` | `str` | Name of the system |
| `pgs` | `list[str]` | Supported primitive gates set of the system. Gate names as described in cQASM (in uppercase). |
| `starttime` | `float` | Timestamp of start-up of the system (return value of `time.time()`) |

##### Get static response example

```jsonc
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

System 2300 publishes dynamic information for 2200 to read. To prevent the system from broadcasting these messages before 2200 is listening and potentially missing relevant information, 2200 can actively start this broadcasting. If necessary, 2200 can also opt to stop the broadcasting.

The schemas for validation can be found in:

* [`/schemas/set_publish/request.schema.json`](../../schemas/set_publish/request.schema.json)
* [`/schemas/set_publish/response.schema.json`](../../schemas/set_publish/response.schema.json)

##### Set publish request payload

| Key | Type | Value |
| --- | --- | --- |
| `active` | `bool` | Turn the PUB/SUB channel on, so that it starts broadcasting. This is a governance safeguard that initial messages are not missed and metadata on results is outdated. |

##### Set publish request example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "set_publish",
    "payload": {
        "active": true
    },
    "version": "0.1.0"
}
```

##### Set publish response payload

This message does not require any additional information in the payload section.

##### Set publish response example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```
