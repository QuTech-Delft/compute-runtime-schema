# Locking

This function consists of two RPCs. One to disable the algorithm interruption and one to enable it again.

## Initialize

This message signals to the 2300 that execution is about to begin. The initialize should be picked up as a request for
locking 2300. However, this interpretation is left to this component.

!!! info
    The schemas for validation inherit from the **extended schema** and can be found in:

    * `/schemas/initialize/request.schema.json`
    * `/schemas/initialize/reply_success.schema.json`
    * `/schemas/initialize/reply_failure.schema.json`

### Initialize request payload

This message does not require any additional information in the payload section.

### Initialize request example

```json title="initialize_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "initialize",
    "version": "0.2.0"
}
```

### Initialize reply payload

This message does not require any additional information in the payload section.

### Initialize reply example

```json title="initialize_reply.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.2.0"
}
```

## Terminate

The opposing message for the initialize request. When 2300 receives this request, execution from user generated circuits
has stopped and the system can resume normal operations.

!!! info
    The schemas for validation inherit from the **extended schema** and can be found in:

    * `/schemas/terminate/request.schema.json`
    * `/schemas/terminate/reply_success.schema.json`
    * `/schemas/terminate/reply_failure.schema.json`

### Terminate request payload

This message does not require any additional information in the payload section.

### Terminate request example

```json title="terminate_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "terminate",
    "version": "0.2.0"
}
```

### Terminate reply payload

This message does not require any additional information in the payload section.

### Terminate reply example

```json title="terminate_reply.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "version": "0.2.0"
}
```
