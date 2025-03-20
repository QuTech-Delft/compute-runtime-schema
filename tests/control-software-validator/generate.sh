#!/bin/bash

# Directory to search
schemas="../../schemas"
models="./models"

# Loop through all files in the schemas directory and subdirectories
find "$schemas" -type f -name "*.json" | while read -r file; do
    filename=$(basename "$file" | sed 's/\..*//')
    parentdir=$(basename "$(dirname "$file")")
    classname="${parentdir}_${filename}"

    datamodel-codegen \
        --input "$file" \
        --class-name $classname \
        --disable-timestamp \
        --input-file-type jsonschema \
        --output "./models/$classname.py" \
        --field-constraints \
        --output-model-type pydantic_v2.BaseModel 
done
