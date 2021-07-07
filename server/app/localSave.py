import hashlib
from datetime import datetime
import os

def saveVideo(src):
    now_time = str(datetime.now())

    hash_ = hashlib.new('sha256')
    hash_.update(now_time.encode())
    directory_name = hash_.hexdigest()

    if not os.path.exists('static/newVideo_{}'.format(directory_name)):
        os.mkdir('static/newVideo_{}'.format(directory_name))

    savePath = 'static/newVideo_{}'.format(directory_name)
    src.save('{}/newVideo_{}.mp4'.format(savePath, directory_name))

    return {'success': True, 'name': directory_name}