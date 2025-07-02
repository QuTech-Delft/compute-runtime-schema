# Locking

This function consists of two RPCs. One to disable the algorithm interruption and one to enable it again.

## Initialize

This message signals to the 2300 that execution is about to begin. The initialize should be picked up as a request for
locking 2300. However, this interpretation is left to this component.

!!! info
    The schemas for validation can be found in:

    * `/schemas/<version>/QuantumHardwareInitializeRequest.schema.json`
    * `/schemas/<version>/QuantumHardwareSimpleSuccessResponse.schema.json`
    * `/schemas/<version>/QuantumHardwareFailureResponse.schema.json`

### Initialize request payload

This message does not require any additional information in the payload section.

### Initialize request example

```json title="initialize_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "initialize",
}
```

### Initialize reply payload

This message does not require any additional information in the payload section.

### Initialize reply example

```json title="initialize_reply.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
}
```

## Terminate

The opposing message for the initialize request. When 2300 receives this request, execution from user generated circuits
has stopped and the system can resume normal operations.

!!! info
    The schemas for validation can be found in:

    * `/schemas/<version>/QuantumHardwareTerminateRequest.schema.json`
    * `/schemas/<version>/QuantumHardwareSimpleSuccessResponse.schema.json`
    * `/schemas/<version>/QuantumHardwareFailureResponse.schema.json`

### Terminate request payload

This message does not require any additional information in the payload section.

### Terminate request example

```json title="terminate_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "terminate",
}
```

### Terminate reply payload

This message does not require any additional information in the payload section.

### Terminate reply example

```json title="terminate_reply.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
}
```
