#!/bin/bash

# Function to pull a model by name
pull_model() {
    local model=$1
    echo "Pulling model ${model}..."
    ollama pull ${model}
    if [ $? -ne 0 ]; then
        echo "Failed to pull model ${model}"
        exit 1
    fi
}

# Start Ollama server in the background
ollama serve &

# Wait for the server to start
echo "Waiting for Ollama server to start..."
sleep 10  # Adjust this value if needed

# Check if the model exists, pull if it doesn't
if ! ollama list | grep -q "${MODEL_NAME}"; then
    pull_model "${MODEL_NAME}"
fi

# Bring the Ollama server to the foreground
wait