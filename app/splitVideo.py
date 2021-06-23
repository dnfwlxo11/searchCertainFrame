import os, cv2

# 비디오로 데이터베이스를 만들고 싶을때
def extractFrame(video, fps):
    vid = cv2.VideoCapture('static/{}/{}.mp4'.format(video, video))
    count = 0

    if not os.path.exists('static/{}/{}'.format(video, video)):
        os.mkdir('static/{}/{}'.format(video, video))
    
    while True:
        ret, image = vid.read()
        
        if (int(vid.get(1)) % fps == 0):
            try:
                cv2.imwrite('static/{}/{}/'.format(video, video) + '{}.jpg'.format(count), image)
                count += 1
            except Exception as e:
                print(e)
            
        if not ret:
            break
            
    vid.release()

    return video