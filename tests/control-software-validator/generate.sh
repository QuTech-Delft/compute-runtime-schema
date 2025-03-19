#!/bin/bash
#
# Directory to search
schemas="../../schemas"
models="./models"

# Loop through all files in the directory and subdirectories
find "$schemas" -type f -name "*.json" | while read -r file; do
    # Extract file name without extension
    filename=$(basename "$file" | sed 's/\..*//')
    # Extract first parent directory
    parentdir=$(basename "$(dirname "$file")")
    classname="${parentdir}_${filename}"
    datamodel-codegen \
        --input "$file" \
        --class-name $classname \
        --disable-timestamp \
        --input-file-type jsonschema \
        --output "./models/$classname.py" \
        --output-model-type pydantic_v2.BaseModel 
done
