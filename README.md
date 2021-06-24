# searchCertainFrame
### Find the time of the desired part in the video
### 영상에서 내가 찾고자 하는 물체를 찾아내주는 서비스

<br>

#### How to install? (어떻게 설치하나?)  
##### 1. If you install with git clone (Whatever you do local or in conda, use comfortable way)  
#####   만약 git clone을 해서 설치를 하는 경우 (로컬 환경이든 conda 환경이든 편한 방법 사용)

```  
git clone https://github.com/dnfwlxo11/searchCertainFrame.git  
cd searchCertainFrame  
pip install -r requirements.txt  
python run.py  
```


##### 2. If you are installing from a docker hub image  
#####    만약 도커 허브에 있는 이미지로 설치를 하는 경우
```
# link : https://hub.docker.com/repository/docker/dnfwlxo11/video_analyze#

docker pull dnfwlxo11/video_analyze:v1  
docker run --rm -it -p 16000:15000 --name=videoAnalyze dnfwlxo11/video_analyze:v1  
```
<br><br>

 - Select the target video and insert the image of the object you want to find in the image  
 (Other models, formulas, fps, resolution, etc. can be adjusted and analyzed by the user.)  
  - 타겟 영상을 선택하고 그 영상에서 찾고자하는 물체 이미지를 넣는다  
  (그 밖의 모델, 공식, fps, 해상도 등의 옵션을 사용자가 조정하여 분석할 수 있다.)  
![searching](https://user-images.githubusercontent.com/32836490/122887925-4f040100-d37c-11eb-84cf-fe766610d811.png)
 
 <br><br>
 
 - It proceeds without page move and guide modal appears.  
 - 페이지 이동없이 진행되며 안내 창이 나온다.  
![searchimg___](https://user-images.githubusercontent.com/32836490/122888243-a013f500-d37c-11eb-837d-f6333973d1df.png)

<br><br>

 - The analysis result is displayed on the right side, and if you click it, you can move to the time and view it in the video in real time.  
 - 우측에 분석 결과가 나오며 클릭시 해당 시간으로 이동하여 실시간으로 영상에서 볼 수 있다.
![complated](https://user-images.githubusercontent.com/32836490/122888381-c89bef00-d37c-11eb-9e6c-85d40450cefd.png)

<br><br>

Both cpu and gpu work, and it is about 60% faster when running on gpu.  
cpu, gpu 모두 동작하며 gpu로 실행시 60퍼센트 정도 빠르다.  
