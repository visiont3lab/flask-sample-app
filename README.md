# Flask samples

This repository provides two different flask examples:

* Upload and Remove file from client to the server
* Process streaming image (aquired using webrtc getUserMedia) using OpenCv

## Setup

```
virtualenv --python=python3 env
source env/bin/activate
pip install -r requirements.txt

# Flask web server
flask run --host=0.0.0.0 --port=5700 

# Python app
python app.py

# Guinicorn
gunicorn -w 1 --log-file=- --bind=0.0.0.0:5700 app:app
```
