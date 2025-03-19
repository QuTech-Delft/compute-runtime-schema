# Control Software Validator

## Introduction

This tool can be used to verify that the control software respects the Compute Runtime Schema.
It will send correctly formatted requests to the control software and verify that responses are correctly formatted as well.

## Usage

After installing the dependencies in requirements.txt,
simply run the following command in the control-software-validator directory:

```bash
pytest .
```

The tool assumes you have the control software running on the same host with its reply channel
available on port 4203 (`tcp://localhost:4203`), and its publish channel available on port 4204 (`tcp://localhost:4204`).
These addresses are configurable using environment variables `HWCS_REQ_ADDRESS` and `HWCS_SUB_ADDRESS`
respectively (or directly in the test file).

## Limitations

There is no way in the protocol to reliably trigger a failure, so the tool can only verify the
correct formatting of successful responses.
