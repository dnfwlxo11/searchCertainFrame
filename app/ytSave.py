from pytube import YouTube
import hashlib
from datetime import datetime

def saveVideo(src):
    yt = YouTube(src)
    hash_ = hashlib.new('sha256')
    hash_.update(str(datetime.now()).encode())

    vids = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()

    savePath = 'static/'
    vids.download(savePath, filename='newVideo_{}'.format(hash_.hexdigest()))

    return hash_