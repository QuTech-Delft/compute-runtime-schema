#!/bin/bash

let max_version=1
while [ -d ../../schemas/v$((max_version+1)) ]; do
    max_version=$((max_version + 1))
done

# Directory to search
schemas="../../schemas/v$max_version"
models="./models"

# Loop through all files in the schemas directory and subdirectories
find "$schemas" -type f -name "*.json" | while read -r file; do
    filename=$(basename "$file" | sed 's/\..*//')

    datamodel-codegen \
        --input "$file" \
        --class-name $filename \
        --disable-timestamp \
        --input-file-type jsonschema \
        --output "./models/$filename.py" \
        --field-constraints \
        --output-model-type pydantic_v2.BaseModel 
done
