from flask import Flask, render_template, request, url_for
from app import similar, ytSave, splitVideo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html/index.html')

@app.route('/api/startAnalyze', methods=['POST', 'GET'])
def getSimilarPart():
    if (request.method == 'POST'):
        request.files['file'], request.form['url']

        videoId = ytSave.saveVideo(request.form['url'])
        videoId = splitVideo.extractFrame('newVideo_{}'.format(videoId))

        request.files['file'].save('static/{}/{}.jpg'.format(videoId, videoId))

        similar.setModel('InceptionV3')

        similar.setImageDB(similar.getImageDB_li(videoId), videoId)
        features, img_path = similar.getFeatureAndPath(videoId)
        result_cos = similar.calc_cossim(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))
        result_eunc = similar.calc_euclienan(features, img_path, 'static/{}/{}.jpg'.format(videoId, videoId))

        result_cos = [(str(k), v) for (k, v) in result_cos]
        result_eunc = [(str(k), v) for (k, v) in result_eunc]

        result_cos.reverse()

    return {'success':'true', 'path': request.form['url'], 'result_cos': result_cos[:10], 'result_eunc': result_eunc[:10], 'len': len(result_cos)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)