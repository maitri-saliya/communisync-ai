#!/bin/bash

echo ""
echo "🚀 Starting CommuniSync..."
echo ""

# Start Ollama if not already running
if ! pgrep -f "ollama serve" > /dev/null
then
    echo "🧠 Starting Ollama..."

    nohup ollama serve \
    > ollama.log 2>&1 &

    sleep 5
else
    echo "🧠 Ollama already running"
fi


# Start Streamlit
if ! pgrep -f "streamlit run app.py" > /dev/null
then
    echo "🌍 Starting Dashboard..."

    nohup streamlit run app.py \
    > dashboard.log 2>&1 &

    sleep 3
else
    echo "🌍 Dashboard already running"
fi


echo ""
echo "✅ CommuniSync Started"
echo ""

echo "Dashboard:"
echo "http://localhost:8501"

echo ""