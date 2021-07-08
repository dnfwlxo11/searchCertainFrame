from pytube import YouTube
import hashlib
from datetime import datetime
import os

def saveVideo(src, fps, resol):
    yt = YouTube(src)

    try:
        if yt.length >= 3600:
            return {'success': False, 'err': 'too long'}

        if not (yt.streams.filter(progressive=True, file_extension='mp4', fps=fps)):
            return {'success': False, 'err': 'none_fps'}
        elif not (yt.streams.filter(progressive=True, file_extension='mp4', res=resol)):
            return {'success': False, 'err': 'none_resol'}
        else:
            now_time = str(datetime.now())
            
            hash_ = hashlib.new('sha256')
            hash_.update(now_time.encode())
            directory_name = hash_.hexdigest()

            if not os.path.exists('static_bac/newVideo_{}'.format(directory_name)):
                os.mkdir('static_bac/newVideo_{}'.format(directory_name))

            vids = yt.streams.filter(progressive=True, file_extension='mp4', res=resol, fps=fps).first()

            savePath = 'static_bac/newVideo_{}'.format(directory_name)
            vids.download(savePath, filename='newVideo_{}'.format(directory_name))

            return {'success': True, 'name': directory_name}
    except Exception as e:
        return Response('{"success": false, "msg": "비디오 저장 중 에러가 발생했습니다."}', status=500, mimetype='application/json')