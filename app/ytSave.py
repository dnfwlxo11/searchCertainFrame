from pytube import YouTube
import hashlib
from datetime import datetime
import os

def saveVideo(src):
    yt = YouTube(src)
    now_time = str(datetime.now())
    
    hash_ = hashlib.new('sha256')
    hash_.update(now_time.encode())
    directory_name = hash_.hexdigest()

    if not os.path.exists('static/newVideo_{}'.format(directory_name)):
        os.mkdir('static/newVideo_{}'.format(directory_name))

    vids = yt.streams.filter(progressive=True, file_extension='mp4', res='360p', fps=24).first()

    savePath = 'static/newVideo_{}'.format(directory_name)
    vids.download(savePath, filename='newVideo_{}'.format(directory_name))

    return directory_name