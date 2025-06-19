#!/bin/bash

let max_version=1
while [ -d ../../schemas/v$((max_version+1)) ]; do
    max_version=$((max_version + 1))
done

echo Test initialize
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareInitializeRequest.schema.json ./data/initialize/request.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareSimpleSuccessResponse.schema.json ./data/initialize/reply.success.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareFailureResponse.schema.json ./data/initialize/reply.failure.json

echo Test terminate
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareTerminateRequest.schema.json ./data/terminate/request.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareSimpleSuccessResponse.schema.json ./data/terminate/reply.success.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareFailureResponse.schema.json ./data/terminate/reply.failure.json

echo Test execute
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareExecuteRequest.schema.json ./data/execute/request.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareExecuteResponse.schema.json ./data/execute/reply.success.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareFailureResponse.schema.json ./data/execute/reply.failure.json

echo Test get_static
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareStaticDataRequest.schema.json ./data/get_static/request.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareStaticDataResponse.schema.json ./data/get_static/reply.success.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareFailureResponse.schema.json ./data/get_static/reply.failure.json

echo Test get_dynamic
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareDynamicDataRequest.schema.json ./data/get_dynamic/request.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareDynamicDataResponse.schema.json ./data/get_dynamic/reply.success.json
check-jsonschema --schemafile ../../schemas/$max_version/QuantumHardwareFailureResponse.schema.json ./data/get_dynamic/reply.failure.json

echo Test publish_state
check-jsonschema --schemafile ../../schemas/max_version/PublishState.schema.json ./data/publish_state/message.json
