# Messages

The message templates that are used for communication between 2200 and 2300 are described below. The base message format
is used for standalone messages, while the extended message format allows to link messages that are technically
independent, but logically connected. These messages are python dictionaries that are converted from/to python strings
via the JSON serializer of the python standard library (`json.loads` and `json.dumps` functions).

## Base message

The message described below has the most basic information needed for standalone messages. JSON schemas will be provided
for these messages and should be inherited from for every relevant message.

!!! info
    The schemas are automatically generated. This means that these requests and replies are already included in the
    schemas. The content is left here to illustrate the basis of the various schemas.

### Base request

| Key | Type | Value |
| --- | --- | --- |
| `command` | `str` | A string identifying the function to be executed. |
| `payload` | `dict` | Arguments for the function to be executed. Presence of this key-value pair depends on the specific command. |

```json title="base_request.json" linenums="1"
{
    "command": "execute",
    "payload": {
        // optional
    },
}
```

### Base reply

| Key | Type | Value |
| --- | --- | --- |
| `status` | `str` | "success" or "failure", depending on whether the command executed successfully. |
| `payload` | `dict` | The return value(s) of the executed command (presence of this key-value pair then depends on the specific command). |
| `payload.error_msg` | `str` | If `"status" == "failure"`: a string describing the failure in more detail. |

#### Base reply success

```json title="base_reply_success.json" linenums="1"
{
    "status": "success",
    "payload": {
        // optional
    },
}
```

#### Base reply failure

```json title="base_reply_failure.json" linenums="1"
{
    "status": "failure",
    "payload": {
        "error_msg": "Lorem ipsum"
    },
}
```

## Extended messages

An extended version of the messages exists. Next to the key-value pairs already present in these messages, it also
contains parameters to link logically-connected messages. JSON schemas will be provided for these messages and should be
inherited from for every relevant message.

!!! info
    The schemas are automatically generated. This means that these requests and replies are already included in the
    schemas. The content is left here to illustrate the basis of the various schemas.

### Extended request

| Key | Type | Value |
| --- | --- | --- |
| `session_id` | `str` | An arbitrary string, filled in in the request, which is copied into the reply object. Normally this would contain a unique identifier for the request, e.g., a UUID |

```json title="extended_request.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "execute",
    "payload": {
        // optional
    },
}
```

### Extended reply

| Key | Type | Value |
| --- | --- | --- |
| `session_id` | `str` | The same `session_id` from the request to link the request and reply. |

```json title="extended_reply.json" linenums="1"
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "payload": {
        // optional
    },
}
```
