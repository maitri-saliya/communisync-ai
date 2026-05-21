#!/bin/bash

echo "Starting Ollama..."
ollama serve &

sleep 5

echo "Starting FastAPI..."
uvicorn server:app --reload &

sleep 3

echo "Starting Streamlit..."
streamlit run app.py &

sleep 3

echo "Starting ngrok..."
ngrok http 8000