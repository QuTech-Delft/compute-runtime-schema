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
    "version": "0.2.0"
}
```

##### Initialize reply payload

This message does not require any additional information in the payload section.

##### Initialize reply example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.2.0"
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
    "version": "0.2.0"
}
```

##### Terminate reply payload

This message does not require any additional information in the payload section.

##### Terminate reply example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.2.0"
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
| `job_id` | `int` | Client defined identifier for the execution. |
| `circuit` | `str` | Circuit description in cQASM language, see below for more information. |
| `include_raw_data` | `bool` | Whether or not to return all bitstrings in the order in which they were measured. |
| `number_of_shots` | `int` | Number of shots to be executed for the circuit. |
| `compile_stage` | `str` | Stage upto which the circuit has already been compiled. |

The cQASM language is described in detail [here](https://www.quantum-inspire.com/kbase/cqasm/). Different
implementations of 2300 might impose different requirements. These will be described on a per case basis.

##### Execute request example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "execute",
    "payload": {
        "job_id": 1,
        "circuit": "version 1.0\n\nqubits 2",
        "include_raw_data": true,
        "number_of_shots": 4
    },
    "version": "0.2.0"
}
```

##### Execute reply payload

| Key | Type | Value |
| --- | --- | --- |
| `job_id` | `int` | Client defined identifier for the execution. |
| `results` | `dict[str, int]` | Mapping of measured bitstring (for a circuit with `n` measurements; `q[n]...q[0]`) to count of occurrences. Limited to `m` results. |
| `raw_data` | `list[str]` | A list of bitstrings (little endian notation; `q[n]...q[0]`) ordered by the shot in which it was measured. If `include_raw_data` is set to `false` the list is left empty. |

##### Execute reply example

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "payload": {
        "job_id": 1,
        "results": {
            "000": 3,
            "001": 1
        },
        "raw_data": [
            "000",
            "001",
            "000",
            "000"
        ]
    },
    "version": "0.2.0"
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
    "version": "0.2.0"
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
| `default_compiler_config` | `dict[str,list[dict[str, Any]]]` | Compiler configurations for different stages. Keys represent stage names (e.g., "decomposition"), and values are list of passes. Each pass includes settings such as the pass name, corresponding method invoked by opensquirrel and additional keyword arguments. |

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
        "starttime": 1690061619.610174,
        "default_compiler_config": {
            "decomposition": [
                {
                    "path": "opensquirrel.decomposer.mckay_decomposer.McKayDecomposer",
                    "method": "decompose",
                    "arguments": {
                        "merge_single_qubit_gates": true
                    }
                }
            ]
        }        
    },
    "version": "0.2.0"
}
```

#### Get dynamic

Dynamic information is generated by 2300. This information can for example constitute calibration data like T1 and T2*.
This dynamic metadata fetched on a status change from `CALIBRATING`/`OFFLINE` to `IDLE` or on startup of 2200.

The schemas for validation inherit from the **base schema** and can be found in:

* [`/schemas/get_dynamic/request.schema.json`](../../schemas/get_dynamic/request.schema.json)
* [`/schemas/get_dynamic/reply.schema.json`](../../schemas/get_dynamic/reply.schema.json)

##### Get dynamic request payload

This message does not require any additional information in the payload section.

##### Get dynamic request example

```jsonc
{
    "command": "get_dynamic",
    "version": "0.2.0"
}
```

##### Get dynamic reply payload

The payload for the message is still under advisement. The appropriate key-value pairs will be filled in when they are
determined.

| Key | Type | Value |
| --- | --- | --- |
| - | - | - |

##### Get dynamic reply example

```jsonc
{
    "status": "success",
    "payload": {
        // to be determined
    },
    "version": "0.2.0"
}
```
