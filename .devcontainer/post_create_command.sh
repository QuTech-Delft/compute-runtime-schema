#!/bin/bash

# Install all packages needed for json validation
pip3 install --user -r ./tests/requirements.txt

# Install packages for generation of fake test messages
npm install -g fake-schema-cli