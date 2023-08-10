#!/bin/bash

echo Test initialize
check-jsonschema --schemafile ../schemas/initialize/request.schema.json ./data/initialize/request.json
check-jsonschema --schemafile ../schemas/initialize/reply.schema.json ./data/initialize/reply.success.json ./data/initialize/reply.failure.json

echo Test terminate
check-jsonschema --schemafile ../schemas/terminate/request.schema.json ./data/terminate/request.json
check-jsonschema --schemafile ../schemas/terminate/reply.schema.json ./data/terminate/reply.success.json ./data/initialize/reply.failure.json

echo Test execute
check-jsonschema --schemafile ../schemas/execute/request.schema.json ./data/execute/request.json
check-jsonschema --schemafile ../schemas/execute/reply.schema.json ./data/execute/reply.success.json ./data/execute/reply.failure.json

echo Test get_static
check-jsonschema --schemafile ../schemas/get_static/request.schema.json ./data/get_static/request.json
check-jsonschema --schemafile ../schemas/get_static/reply.schema.json ./data/get_static/reply.success.json ./data/get_static/reply.failure.json

echo Test get_dynamic
check-jsonschema --schemafile ../schemas/get_dynamic/request.schema.json ./data/get_dynamic/request.json
check-jsonschema --schemafile ../schemas/get_dynamic/reply.schema.json ./data/get_dynamic/reply.success.json ./data/get_dynamic/reply.failure.json

echo Test publish_state
check-jsonschema --schemafile ../schemas/publish_state/message.schema.json ./data/publish_state/message.json
