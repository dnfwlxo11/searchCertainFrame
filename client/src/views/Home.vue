<template>
  <div class="home">
    <div class="container p-3">
      <div v-if="progress" class="progress-modal">
        <div class="progress-modal-content">
          <img src="../assets/progressBar.gif" alt="loading...">
          <p>로딩 중이며 재생 시간이 길수록 많은 시간이 소요됩니다.</p>
        </div>
      </div>
      <div class="row">
        <div class="col-md-8 mb-5">
          <div class="btn-group btn-group-toggle mb-3" data-toggle="buttons">
            <label class="btn btn-outline-primary active">
              <input type="radio" name="options" id="option1" value="유튜브" @click="setMode" checked>유튜브
            </label>
            <label class="btn btn-outline-primary">
              <input type="radio" name="options" id="option2" value="내영상" @click="setMode">내 영상
            </label>
          </div>
          <h4>찾을 동영상</h4>
          <div v-if="!mode" class="row mb-5">
            <div class="col-12 embed-responsive embed-responsive-16by9 mb-3">
              <iframe class="embed-responsive-item" :src="youtubeVideo" frameborder="0"></iframe>
            </div>
            <input class="col-8 mr-3" type="text" placeholder="유튜브 동영상 주소를 입력해주세요." v-model="youtubeUrl"></input>
            <button class="btn btn-primary col-3" @click="getYoutubeVideo">동영상 가져오기</button>
          </div>
          <div v-else class="row mb-5">
            <div class="col-12 embed-responsive embed-responsive-16by9 mb-3">
              <video class="embed-responsive-item" :src="localUrl" @click="$refs.localVideoFile.click()" controls>
                <source :src="localVideo" type="video/mp4">
              </video>
            </div>
            <input name="input-video" type="file" accept="video/*" ref='localVideoFile' style="display: none" @change="uploadVideo"></input>
          </div>
          <div class="row">
            <div class="input-group col-md-6">
              <h4>찾고자 하는 대상</h4>
              <div class="embed-responsive embed-responsive-16by9 mb-3">
                <a href="javascript:;" class="d-block" @click="$refs.inputImgFile.click()">
                  <img class="embed-responsive-item" :src="thumbnail">
                </a>
              </div>
              <input class="mb-3" name='thumbnail' ref="inputImgFile" type="file" accept="image/*" style="visibility: hidden" @change="uploadImage">
            </div>
            <div class="col-md-6 m-auto">
              <div>
                <button class="btn btn-block btn-warning" @click="startAnalyze">분석 시작</button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4 mt-3">
          <div class="ml-3 mb-5">
            <div class="mb-3">
              <label @click="setSpeed">
                <input type="checkbox" name="color" value="blue">스피드 모드
              </label>
            </div>
            <div class="mb-3">
              <h4>예측 모델</h4>
              <select v-model="model">
                <option value="VGG16">VGG16</option>
                <option value="ResNet50">ResNet50</option>
                <option value="InceptionV3">InceptionV3</option>
                <option value="EfficientNet-B0">EfficientNet-B0</option>
              </select>
            </div>
            <div class="mb-3">
              <h4>유사도 공식</h4>
              <input type="radio" name="similar_calc" value="cosc" v-model="calc">Cosin 유사도
              <input type="radio" name="similar_calc" value="eunc" v-model="calc">Euclidian 유사도
            </div>
            <div v-if="!speed" class="mb-3">
              <h4>FPS</h4>
              <input type="radio" name="video_fps" value="24" v-model="fps">24FPS
              <input type="radio" name="video_fps" value="30" v-model="fps">30FPS
              <input type="radio" name="video_fps" value="60" v-model="fps">60FPS
            </div>
            <div v-if="!speed" class="mb-3">
              <h4>해상도</h4>
              <input type="radio" name="video_res" value="240p" v-model="resol">240p
              <input type="radio" name="video_res" value="360p" v-model="resol">360p
              <input type="radio" name="video_res" value="480p" v-model="resol">480p
              <input type="radio" name="video_res" value="720p" v-model="resol">720p
            </div>
            <div class="mb-3">
              <h4>결과값 개수</h4>
              <input type="radio" name="predict_li" value="3" v-model="listSize">3개
              <input type="radio" name="predict_li" value="5" v-model="listSize">5개
              <input type="radio" name="predict_li" value="10" v-model="listSize">10개
              <input type="radio" name="predict_li" value="20" v-model="listSize">20개
              <input type="radio" name="predict_li" value="30" v-model="listSize">30개
            </div>
          </div>
          <div class="row overflow-auto" style="max-height: 400px">
            <ul class="list-group" v-if="isData">
              <li class="list-group-item" v-for="(item, index) of analyzeData" :key="index">
                <a class="" v-if="!mode" @click="youtubeVideo = item[0]">{{ item[1] }}</a>
                <a class="" v-else @click="localUrl = localUrl.split('t=')[0] + 't=' + item[0]">{{ item[1] }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Home',

    data() {
      return {
        thumbnail: require('../assets/thumbnail.png'),
        thumbnailFile: '',
        youtubeVideo: 'https://youtube.com/embed',
        youtubeUrl: '',
        localVideo: require('../assets/thumbnail.png'),
        localUrl: '',
        progress: false,
        speed: false,
        mode: false,
        model: 'VGG16',
        calc: 'cosc',
        fps: '30',
        resol: '360p',
        listSize: '5',
        analyzeData: [],
        isData: false
      }
    },

    methods: {
      getYoutubeVideo() {
        const id = new URL(this.youtubeUrl).search.split('=')[1];
        this.youtubeVideo = `https://youtube.com/embed/${id}`
      },

      setSpeed() {
        this.speed = !this.speed;
      },

      setMode(e) {
        console.log(e.target.value)
        if (e.target.value == '유튜브') {
          this.mode = false;
          this.localVideo = '../assets/thumbnail.png';
          this.localUrl = '';
          this.analyzeData = [];
          this.isData = false;
        } else {
          this.mode = true;
          this.youtubeVideo = 'https://youtube.com/embed';
          this.youtubeUrl = '';
          this.analyzeData = [];
          this.isData = false;
        }
      },

      setProgress() {
        this.progress = !this.progress
      },

      uploadImage(e) {
        const reader = new FileReader();

        if (e.target.files[0] !== undefined) {
          reader.readAsDataURL(e.target.files[0]);
          this.thumbnailFile = e.target.files[0];

          reader.onload = () => {
            this.thumbnail = reader.result;
          }
        } else {
          alert('비디오가 로딩되지 않았습니다.')
        }
      },

      uploadVideo(e) {
        const reader = new FileReader();

        this.setProgress();

        if (e.target.files[0] !== undefined) {
          reader.readAsDataURL(e.target.files[0]);
          this.localVideo = e.target.files[0]

          reader.onload = () => {
            this.localUrl = `${reader.result}#t=0.1`;
          }

          this.setProgress();
        } else {
          alert('비디오가 로딩되지 않았습니다.')
          this.setProgress();
        }
      },

      async startAnalyze() {
        this.setProgress()

        this.analyzeData = [];

        const sendData = {
          thumbnail: this.thumbnailFile,
          type: !this.mode ? 'youtube' : 'local',
          model: this.model,
          calc: this.calc,
          fps: this.fps,
          len: this.listSize,
          resol: this.resol,
          url: !this.mode ? this.youtubeVideo : this.localVideo,
          mode: this.speed ? 'speed' : 'normal'
        }

        const form = new FormData()
        for (let key in sendData)
          form.append(key, sendData[key]);

        let res = await axios({
          url: 'http://192.168.0.106:5000/api/startAnalyze',
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          data: form
        })
        .catch((err) => {
          this.setProgress();
          const resErr = err.response.data.msg
          alert(resErr)
          window.location.href = '/'
        })

        this.analyzeData = res.data.result.reduce((acc, item) => {
          let time = item[1].split('.')[0];

          if (sendData.type == 'youtube') {
            item = [`${this.youtubeVideo}?autoplay=1&start=${time}`,
              `${Math.floor(time/60) > 9  ? Math.floor(time/60) : '0' + Math.floor(time/60)} : ${time%60 > 9 ? time%60 : '0' + time%60 }`
            ]
          } else {
            item = [time,
              `${Math.floor(time/60) > 9  ? Math.floor(time/60) : '0' + Math.floor(time/60)} : ${time%60 > 9 ? time%60 : '0' + time%60 }`
            ]
          }

          acc.push(item)

          return acc
        }, []);

        this.isData = true;
        this.setProgress();
      }
    }
  }
</script>

<style>
  li {
    list-style: none;
  }

  .progress-modal {
    opacity: 1.0;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.4);
  }

  .progress-modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 50%;
  }

  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
</style>