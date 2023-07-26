# Interface

The job processor (2200) and control-software (2300) are python software components that run in different python
processes either on the same or different PCs. The interface consists of the following functions:

* Locking: Function to avoid 2300 interrupting a 2200 algorithm.
* Execution: Function to execute algorithm.
* Meta communication: Function to retrieve system information from 2300

Although this ICD was originally intended for a spin quantum runtime, an effort was made to make this a generic
interface that can easily be extended to other quantum runtimes. To achive this the functions above will be performed in
two different communication modi; request/reply and publish/subscribe. The interface for both modi consists of two
layers: a message layer and an application layer.

* [Request/Reply](request/index.md)
* [Publish/Subscribe](publish/index.md)
