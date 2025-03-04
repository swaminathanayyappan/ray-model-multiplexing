#!/bin/bash


FILE_PATH="manifests/app-build-config.yaml"
COMMAND="serve build -d app/ model_multiplex_app.app test_app.app -o manifests/app-build-config.yaml"

# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Build config file doesn't exist at: $FILE_PATH"
    echo "Creating new build file"
    eval $COMMAND
    echo "Build config file created successfully at: $FILE_PATH"
else
    echo "Build config file already exists at : $FILE_PATH"
    echo "Skipping build file creation"
fi
