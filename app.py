from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from core import image_retraining
from os.path import join
import utils
from decimal import Decimal
import os



app = Flask(__name__)
CORS(app)
app.config['DELETE_DATASET_SINGLE_PREDICTION'] = 'rm -rf static/img/single_prediction/*'
app.config['FOLDER_DATASET_SINGLE_PREDICTION'] = 'static/img/single_prediction/'


@app.route('/', methods=['GET'])
def api_root():
    msg = 'Image-Retraining-Classification permite etiquetar una nueva imagen de un documento de identificación institucional'
    return render_template('index.html', msg=msg)

@app.route('/file-upload/<type>', methods=['POST'])
def file_upload_positive(type):
    new_file = request.files.get('file', None)
    file_name = new_file.filename
    if new_file is not None:
        if type == 'classification':
            os.system(app.config['DELETE_DATASET_SINGLE_PREDICTION'])
            new_file.save(join(app.config['FOLDER_DATASET_SINGLE_PREDICTION'], file_name))
            response = jsonify({'success': True})
        else:
            response = jsonify({'success': False, 'msg': 'invalid-type'})
            response.status_code = 400
            pass
        return response
    response = jsonify({'success': False, 'msg': 'file-upload-is-none'})
    response.status_code = 400
    return response


@app.route('/classification', methods=['POST'])
def classification():
    images_prediction = utils.get_images(app.config['FOLDER_DATASET_SINGLE_PREDICTION'])
    url_image = ''
    for image_prediction in images_prediction:
        url_image = image_prediction
    response_image_retraining = image_retraining.classification()
    if response_image_retraining['success'] == True:
        return render_template('index.html', predict=True, url_image=url_image, class_1=response_image_retraining['class-1'], score_1=response_image_retraining['score-1'], class_2=response_image_retraining['class-2'], score_2=response_image_retraining['score-2'])
    else:
        response = jsonify({'success': False, 'msg': 'error-classification-image-retraining'})
        response.status_code = 400


if __name__ == "__main__":
#    context = ('/etc/letsencrypt/live/loencontre.co/fullchain.pem', '/etc/letsencrypt/live/loencontre.co/privkey.pem')
 #   app.run(host='0.0.0.0', debug=True, port=5000, ssl_context=context)
    app.run(host='0.0.0.0', debug=True, port=5000)
