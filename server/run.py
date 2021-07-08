from flask import Flask, render_template, request, url_for, Response
from app import similar, ytSave, splitVideo, localSave
from flask_cors import CORS

app = Flask(__name__, static_url_path="/", static_folder="static")
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/startAnalyze', methods=['POST', 'GET'])
def getSimilarPart():
    req = request.form
    print('1')

    if (request.method == 'POST'):
        print('2')
        try:
            if (req['type'] == 'youtube'):
                videoId = ytSave.saveVideo(req['url'], int(req['fps']), req['resol'])
            else:
                videoId = localSave.saveVideo(request.files['url'])
        except Exception as e:
            print(e)
            return Response('{"success": false, "msg": "옵션 중 비디오가 지원하지 않는 옵션이 있습니다. 옵션을 변경해주세요."}', status=500, mimetype='application/json')

        if (videoId['success']):
            videoId = splitVideo.extractFrame('newVideo_{}'.format(videoId['name']), int(req['fps']))
            print('3')
            try:
                request.files['thumbnail'].save('static_bac/{}/{}.jpg'.format(videoId, videoId))
            except Exception as e:
                print(e)
                return Response('{"success": false, "msg": "검색 이미지 저장 중 에러가 발생했습니다."}', status=500, mimetype='application/json')
            print('4')
            try:
                similar.setModel(req['model'])
                similar.setImageDB(similar.getImageDB_li(videoId), videoId)
            except Exception as e:
                print(e)
                return Response('{"success": false, "msg": "비디오 분석 중 에러가 발생했습니다."}', status=500, mimetype='application/json')

            print('5')  
            try:
                if (req['mode'] == 'speed'):
                    features, img_path = similar.speedMode(videoId, 'static_bac/{}/{}.jpg'.format(videoId, videoId), int(req['len']))
                else:
                    features, img_path = similar.getFeatureAndPath(videoId)
            except Exception as e:
                print(e)
                return Response('{"success": false, "msg": "실행 모드 설정 중 에러가 발생했습니다."}', status=500, mimetype='application/json')

            print('6')
            try:
                if (req['calc'] == 'cosc'):
                    result_cos = similar.calc_cossim(features, img_path, 'static_bac/{}/{}.jpg'.format(videoId, videoId))
                    result_cos = [(str(k), v) for (k, v) in result_cos]

                    result_cos.reverse()

                    return {'success': True, 'result': result_cos[:int(req['len'])], 'len': len(result_cos), 'mode': 'cos'}
                elif (req['calc'] == 'eucl'):
                    result_eucl = similar.calc_euclienan(features, img_path, 'static_bac/{}/{}.jpg'.format(videoId, videoId))
                    result_eucl = [(str(k), v) for (k, v) in result_eucl]

                    return {'success': True, 'result': result_eucl[:int(req['len'])], 'len': len(result_eucl), 'mode': 'eucl'}
            except Exception as e:
                print(e)
                return Response('{"success": false, "msg": "유사도 비교 중 에러가 발생했습니다."}', status=500, mimetype='application/json')

if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
    