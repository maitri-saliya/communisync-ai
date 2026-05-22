#!/bin/bash

echo ""
echo "🛑 Stopping CommuniSync..."
echo ""


pkill -f "streamlit run app.py"

pkill -f "ollama serve"


echo "✅ Stopped"
echo ""