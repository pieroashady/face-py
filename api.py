from app import app
from face_rec import classify_face
import os
from flask import Flask, redirect, jsonify, session
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# extensi file yang di izinkan
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# dapatkan nama file dan extensinya
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def Upload():
    name = request.form['name']
    nik = request.form['nik']
    

    if 'image_url' not in request.files:
        response = jsonify({'message': 'tidak ada gambar'})
        response.status_code = 400
        return response
    
    file = request.files['image_url']
    if file == '':
        response = jsonify({'message': 'gambar belum di upload'})
        response.status_code = 400
        return response

    if allowed_file(file.filename) == True:
        file_name = secure_filename(file.filename)
        path = nik + '_' + name
        if not os.path.exists(os.path.abspath('dataset')):
            os.mkdir(os.path.abspath('dataset'))
        if not os.path.exists(os.path.abspath('dataset\\' + path)):
            os.mkdir(os.path.abspath('dataset\\' + path))
        if os.path.exists(os.path.abspath('dataset\\' + path)):
            dir_dataset = os.path.abspath('dataset\\' + path)
            with open(dir_dataset + '/' + name + '.jpg', 'wb') as data:
                image_url = request.files['image_url']
                for i in image_url:
                    data.write(i)
        data = {
                'status': 200,
                'message': 'Record inserted successfuly',
                'data' : {
                    'nik': nik,
                    'name': name
                }
            }
    # else :
    #     data = {
    #         'status': 400,
    #         'message': 'Record Inserted Failed'
    #     }
        return jsonify(data)

@app.route('/facereco', methods=['POST'])
def Facereco():
    file = request.files['image_url']
        
    if file == '':
        response = jsonify({'message': 'gambar belum di upload'})
        response.status_code = 400
        return response
    if allowed_file(file.filename) == True:
        file_name = secure_filename(file.filename)
        file.save(os.path.join('images/', file_name))
        path_image = 'images/' + file_name
        data = classify_face(path_image)
        response = {
            'status': True,
            'name': data
        }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)