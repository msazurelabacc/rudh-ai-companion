#!/bin/bash
echo "🚀 Starting Rudh AI Video Studio"
cd /home/site/wwwroot
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
