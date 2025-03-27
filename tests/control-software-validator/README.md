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
These addresses are configurable using environment variables `CSV_HWCS_REQ_ADDRESS` and `CSV_HWCS_SUB_ADDRESS`
respectively (or directly in the test file).

Setting the environment variable `CSV_MODE` to `dry_run` triggers a dry run that does not connect to the control software.
This is useful for verifying the validator itself, as it will fail if any of the request messages are badly formatted.

## Model generation

The models used in the validator are automatically generated based on the jsonschemas. The generate.sh script can be run
in the same Python environment as the tool.

## Limitations

There is no way in the protocol to reliably trigger a failure, so the tool can only verify the
correct formatting of successful responses.
