# Messages

The message templates that are used for communication between 2200 and 2300 are described below. The various functions
of the systems can be divided between user-triggered communication and system communication. User-triggered
communication for example is the execution of an algorithm, while system communication is fetching static system
information. These messages are python dictionaries that are converted from/to python strings via the JSON serializer of
the python standard library (`json.loads` and `json.dumps` functions).

## Base message

The message described below has the most basic information needed for a message, either for requests or publish. The
information contained within these messages is sufficient for non-iterative communication, e.g. requesting system
information. These messages would be sent only once and not be part of a longer session.

### Base request

| Key | Type | Value |
| --- | --- | --- |
| `command` | `str` | A string identifying the function to be executed. |
| `payload` | `dict` | Arguments for the function to be executed. Presence of this key-value pair depends on the specific command. |
| `version` | `str` | String containing the version number of the message format. This allows modification of the interface in a backwards compatible manner. The version will adhere to the [semantic versioning rules](<https://semver.org/>). Presently we are still using a beta numbering (`0.y.z`). |

```jsonc
{
    "command": "execute",
    "payload": {
        // optional
    },
    "version": "0.1.0"
}
```

### Base reply

| Key | Type | Value |
| --- | --- | --- |
| `status` | `str` | "success" or "failure", depending on whether the command executed successfully. |
| `payload` | `dict` | If "status" == "failure": a string describing the failure in more detail. If "status" == "success": the return value(s) of the executed command (presence of this key-value pair then depends on the specific command). |
| `version` | `str` | String containing the version number of the message format. This allows modification of the interface in a backwards compatible manner. The version will adhere to the [semantic versioning rules](<https://semver.org/>). Presently we are still using a beta numbering (`0.y.z`). |

```jsonc
{
    "status": "success",
    "payload": {
        // optional
    },
    "version": "0.1.0"
}
```

## Extended messages

An extended version of the messages exists. Next to the key-value pairs already present in these messages, it also
contains session identifiers. These session identifiers are needed when messages repetitively transcend application
boundaries and should be tracked as such (e.g. execution of jobs).

### Extended request

| Key | Type | Value |
| --- | --- | --- |
| `session_id` | `str` | An arbitrary string, filled in in the request, which is copied into the response object. Normally this would contain a unique identifier for the request, e.g., a UUID |

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "command": "execute",
    "payload": {
        // optional
    },
    "version": "0.1.0"
}
```

### Extended reply

| Key | Type | Value |
| --- | --- | --- |
| `session_id` | `str` | The same `session_id` from the request to validate the request and reply. |

```jsonc
{
    "session_id": "eb4fdc2c-755b-47d8-af76-bbca2dce554d",
    "status": "success",
    "payload": {
        // optional
    },
    "version": "0.1.0"
}
```
