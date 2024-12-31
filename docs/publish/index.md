# Publish/Subscribe

For publish/subscribe, a broadcast model is followed. 2300 acts as a sender, while 2200 listens to the various messages.

## Message layer

| Property | Value |
| --- | --- |
| Middleware | [ZMQ sockets](<https://zeromq.org>) version 4.x |
| ZMQ message pattern | Publish-subscribe. 2200 using SUB socket and 2300 PUB socket |
| Publish binding argument | `tcp://*:4204` i.e., uses underlying TCP socket connect to port 4204. |
| Subscriber connect argument | `tcp://<host address>:4204`. The `<host address>` contains the IP address of 2300. |

The messages in this section inherit from generic messages described in the [messages spec](../messages.md). Since
messages will only be broadcasted, only the [base request](../messages.md#base-request) will be used. Any new messages
should also inherit from this message.

## Application layer

The application layer contains the specific application functions that are described in the
[root document](../index.md). The functions are described via the contents of the published dictionaries.
