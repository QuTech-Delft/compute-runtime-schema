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
