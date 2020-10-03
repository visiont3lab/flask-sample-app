import os
from flask import Flask, render_template, make_response, jsonify, request, redirect, url_for, abort, send_from_directory
import base64
import cv2 
import numpy as np

'''
Example: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
Doc: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
'''
app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 2024 * 2024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('upload.html', files=files)

@app.route('/realtime',methods=['GET'])
def realtime():
    return render_template('realtime.html')


@app.route('/realtime',methods=['POST'])
def process():
    data_url = request.form.get('name')
    base64_img = data_url.replace('data:image/png;base64,','')
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    # Opencv
    nparr = np.fromstring(decoded_image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    retval, buffer = cv2.imencode('.png', gray)
    text = 'data:image/png;base64,' + base64.b64encode(buffer).decode('utf-8')
    d = jsonify({"value": text})
    return  render_template('realtime.html', image_url=text)
    #return  make_response(jsonify(d), 200)

@app.route('/uploads', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file[]") #request.files['file']
    for uploaded_file in uploaded_files:
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    path = os.path.join(app.config['UPLOAD_PATH'], filename)
    os.remove(path)
    return redirect(url_for('index'))
