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

echo Test trigger_publish
check-jsonschema --schemafile ../schemas/trigger_publish/request.schema.json ./data/trigger_publish/request.json
check-jsonschema --schemafile ../schemas/trigger_publish/reply.schema.json ./data/trigger_publish/reply.success.json ./data/trigger_publish/reply.failure.json

echo Test publish_state
check-jsonschema --schemafile ../schemas/publish_state/request.schema.json ./data/publish_state/request.json

echo Test publish_dynamic
check-jsonschema --schemafile ../schemas/publish_dynamic/request.schema.json ./data/publish_dynamic/request.json
