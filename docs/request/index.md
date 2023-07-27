# Request/Reply

For request/reply, the interface will be a client-server interface. 2200 acts as the client and 2300 as the server. It
follows the semantics of remote procedure calls (RPCs), i.e., the client "calls" a function that is "remotely" executed
on the server and the result is passed back to the client.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Request-reply. 2200 using REQ socket and 2300 REP socket |
| Server binding argument | `tcp://*:4203` i.e., uses underlying TCP socket connect to port 4203. |
| Client connect argument | `tcp://<host address>:4203`. The `<host address>` contains the IP address of 2300. |

The messages in this section inherit from generic messages described in the [messages spec](../messages.md). Any new
messages should also inherit from these messages.

## Application layer

The application layer contains the specific application functions that are described in the
[root document](../index.md). The functions are described via the contents of the request and reply dictionaries.

### Locking

This function consists of two RPCs. One to disable the algorithm interruption and one to enable it again.

#### Initialize

This message signals to the 2300 that execution is about to begin. The initialize should be picked up as a request for
locking 2300. However, this interpretation is left to this component.

The schemas for validation inherit from the **extended schema** and can be found in:

* [`/schemas/initialize/request.schema.json`](../../schemas/initialize/request.schema.json)
* [`/schemas/initialize/reply.schema.json`](../../schemas/initialize/reply.schema.json)

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

##### Initialize reply payload

This message does not require any additional information in the payload section.

##### Initialize reply example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

#### Terminate

The opposing message for the initialize request. When 2300 receives this request, execution from user generated circuits
has stopped and the system can resume normal operations.

The schemas for validation inherit from the **extended schema** and can be found in:

* [`/schemas/terminate/request.schema.json`](../../schemas/terminate/request.schema.json)
* [`/schemas/terminate/reply.schema.json`](../../schemas/terminate/reply.schema.json)

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

##### Terminate reply payload

This message does not require any additional information in the payload section.

##### Terminate reply example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.1.0"
}
```

### Execution

Execute an algorithm on 2300. This is only allowed when 2300 is in non-interruption mode. So for a single execution
three commands are required, "initialize", "execute", "terminate".

#### Execute

This message requests a backend to execute a user generated circuit. This can only be done when the system has been
initialized (in reality "locked").

The schemas for validation inherit from the **extended schema** and can be found in:

* [`/schemas/execute/request.schema.json`](../../schemas/execute/request.schema.json)
* [`/schemas/execute/reply.schema.json`](../../schemas/execute/reply.schema.json)

##### Execute request payload

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `circuit` | `str` | Circuit description in cQASM language, see below for more information. |
| `number_of_shots` | `int` | Number of shots to be executed for the circuit. |

The cQASM language is described in detail [here](https://www.quantum-inspire.com/kbase/cqasm/). 2300 imposes the
following constraints on the cQASM it accepts:

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

##### Execute reply payload

| Key | Type | Value |
| --- | --- | --- |
| `run_id` | `int` | Client defined identifier for the execution. |
| `results` | `dict[str, int]` | Mapping of measured bitstring (little endian notation; `q[n]...q[0]`) to count of occurrences. |

##### Execute reply example

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

System information from 2300 is divided over both request/reply and publish/subscribe. The messages below are published
by 2300.

#### Get static

Get system information from 2300. This information is retrieved only once, normally at startup time for 2200.

The schemas for validation inherit from the **base schema** and can be found in:

* [`/schemas/get_static/request.schema.json`](../../schemas/get_statis/request.schema.json)
* [`/schemas/get_static/reply.schema.json`](../../schemas/get_static/reply.schema.json)

##### Get static request payload

This message does not require any additional information in the payload section.

##### Get static request example

```jsonc
{
    "command": "get_static",
    "version": "0.1.0"
}
```

##### Get static reply payload

| Key | Type | Value |
| --- | --- | --- |
| `nqubits` | `int` | The number of qubits |
| `topology` | `list[tuple]` | List of the edges between the various qubits |
| `name` | `str` | Name of the system |
| `pgs` | `list[str]` | Supported primitive gates set of the system. Gate names as described in cQASM (in uppercase). |
| `starttime` | `float` | Timestamp of start-up of the system (return value of `time.time()`) |

##### Get static reply example

```jsonc
{
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

#### Trigger publish

System 2300 publishes dynamic information for 2200 to read. It might happen that 2300 broadcasted a message while 2200
wasn't ready yet, resulting in relevant information being missed. In such a case, 2200 can request 2300 to publish the
information again.

The schemas for validation inherit from the **base schema** and can be found in:

* [`/schemas/trigger_publish/request.schema.json`](../../schemas/trigger_publish/request.schema.json)
* [`/schemas/trigger_publish/reply.schema.json`](../../schemas/trigger_publish/reply.schema.json)

##### Set publish request payload

This message does not require any additional information in the payload section.

##### Set publish request example

```jsonc
{
    "command": "trigger_publish",
    "version": "0.1.0"
}
```

##### Set publish reply payload

This message does not require any additional information in the payload section.

##### Set publish reply example

```jsonc
{
    "status": "success",
    "version": "0.1.0"
}
```
