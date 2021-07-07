from flask import Flask, render_template, request, url_for
from app import similar, ytSave, splitVideo, localSave

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/api/startAnalyze', methods=['POST', 'GET'])
def getSimilarPart():
    req = request.form

    if (request.method == 'POST'):
        if (req['type'] == 'youtube'):
            videoId = ytSave.saveVideo(req['url'], int(req['fps']), req['resol'])
        else:
            videoId = localSave.saveVideo(request.files['inputVideo'])

        if (videoId['success']):
            videoId = splitVideo.extractFrame('newVideo_{}'.format(videoId['name']), int(req['fps']))

            request.files['thumbnail'].save('static/{}/{}.jpg'.format(videoId, videoId))

            similar.setModel(req['model'])
            similar.setImageDB(similar.getImageDB_li(videoId), videoId)

            if (req['mode'] == 'speed'):
                features, img_path = similar.speedMode(videoId, 'static/{}/{}.jpg'.format(videoId, videoId), int(req['len']))
            else:
                features, img_path = similar.getFeatureAndPath(videoId)

            if (req['calc'] == 'cos'):
                result_cos = similar.calc_cossim(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))
                result_cos = [(str(k), v) for (k, v) in result_cos]

                result_cos.reverse()

                return {'success': True, 'result_cos': result_cos[:int(req['len'])], 'len': len(result_cos), 'mode': 'cos'}
            elif (req['calc'] == 'eucl'):
                result_eucl = similar.calc_euclienan(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))
                result_eucl = [(str(k), v) for (k, v) in result_eucl]

                return {'success': True, 'result_eucl': result_eucl[:int(req['len'])], 'len': len(result_eucl), 'mode': 'eucl'}
        else:
            return {'success': False, 'err': videoId['err']}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)