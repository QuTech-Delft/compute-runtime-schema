# Execution

Execute an algorithm on 2300. This is only allowed when 2300 is in non-interruption mode. So for a single execution
three commands are required, "initialize", "execute", "terminate".

## Execute

This message requests a backend to execute a user generated circuit. This can only be done when the system has been
initialized (in reality "locked").

!!! info
    The schemas for validation  can be found in:

    * `/schemas/<version>/QuantumHardwareExecuteRequest.schema.json`
    * `/schemas/<version>/QuantumHardwareExecuteResponse.schema.json`
    * `/schemas/<version>/QuantumHardwareFailureResponse.schema.json`

### Execute request payload

| Key | Type | Value |
| --- | --- | --- |
| `job_id` | `int` | Client defined identifier for the execution. |
| `circuit` | `str` | Circuit description in cQASM language, see below for more information. |
| `include_raw_data` | `bool` | Whether or not to return all bitstrings in the order in which they were measured. |
| `number_of_shots` | `int` | Number of shots to be executed for the circuit. |

The cQASM language is described in detail [here](https://qutech-delft.github.io/cQASM-spec/latest/). Different
implementations of 2300 might impose different requirements. These will be described on a per case basis.

### Execute request example

```json title="execute_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "execute",
    "payload": {
        "job_id": 1,
        "circuit": "version 3.0\n\nqubits[2] q",
        "include_raw_data": true,
        "number_of_shots": 4
    },
    "version": "0.2.0"
}
```

### Execute reply payload

| Key | Type | Value |
| --- | --- | --- |
| `job_id` | `int` | Client defined identifier for the execution. |
| `results` | `dict[str, int]` | Mapping of measured bitstring (for a circuit with `n` measurements; `q[n]...q[0]`) to count of occurrences. Limited to `m` results. |
| `raw_data` | `list[str]` | A list of bitstrings (little endian notation; `q[n]...q[0]`) ordered by the shot in which it was measured. If `include_raw_data` is set to `false` the list is left empty. |

### Execute reply example

```json title="execute_reply.json" linenums="1"
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
