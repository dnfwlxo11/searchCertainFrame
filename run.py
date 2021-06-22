from flask import Flask, render_template, request, url_for
from app import similar, ytSave, splitVideo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/api/startAnalyze', methods=['POST', 'GET'])
def getSimilarPart():
    req = request.form

    if (request.method == 'POST'):
        videoId = ytSave.saveVideo(req['url'], int(req['fps']), req['resol'])

        if (videoId['success']):
            videoId = splitVideo.extractFrame('newVideo_{}'.format(videoId['name']), int(req['fps']))

            request.files['file'].save('static/{}/{}.jpg'.format(videoId, videoId))

            similar.setModel(req['model'])

            similar.setImageDB(similar.getImageDB_li(videoId), videoId)
            features, img_path = similar.getFeatureAndPath(videoId)

            if (req['calc'] == 'cos'):
                result_cos = similar.calc_cossim(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))
                result_cos = [(str(k), v) for (k, v) in result_cos]

                result_cos.reverse()

                return {'success': True, 'path': req['url'], 'result_cos': result_cos[:int(req['len'])], 'len': len(result_cos)}
            elif (req['calc'] == 'eunc'):
                result_eunc = similar.calc_euclienan(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))
                result_eunc = [(str(k), v) for (k, v) in result_eunc]

                return {'success': True, 'path': req['url'], 'result_cos': result_eunc[:int(req['len'])], 'len': len(result_eunc)}
        else:
            return {'success': False, 'err': videoId['err']}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)