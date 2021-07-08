import os, cv2, math

# 비디오로 데이터베이스를 만들고 싶을때
def extractFrame(video, fps):
    vid = cv2.VideoCapture('static_bac/{}/{}.mp4'.format(video, video))
    count = 0

    if not os.path.exists('static_bac/{}/{}'.format(video, video)):
        os.mkdir('static_bac/{}/{}'.format(video, video))
    
    if (vid.get(cv2.CAP_PROP_FPS)):
        fps = math.floor(vid.get(cv2.CAP_PROP_FPS))

    while True:
        ret, image = vid.read()
        
        if (int(vid.get(1)) % fps == 0):
            try:
                cv2.imwrite('static_bac/{}/{}/'.format(video, video) + '{}.jpg'.format(count), image)
                count += 1
            except Exception as e:
                print(e)
            
        if not ret:
            break
            
    vid.release()

    return video