const img_file = document.getElementById('img-file'),
    video_file = document.getElementById('video-file'),
    player = document.getElementById('player'),
    local_player = document.getElementById('local-player'),
    video_source = document.getElementById('video-source'),
    link = document.getElementById('video-link'),
    hidden_url = document.getElementById('hidden-url'),
    thumbnail = document.getElementById('thumbnail'),
    result_ul = document.getElementById('result-ul'),
    model = document.getElementById('model'),
    calc = document.getElementsByName('similar_calc'),
    resol = document.getElementsByName('video_res'),
    fps = document.getElementsByName('video_fps'),
    len = document.getElementsByName('predict_li'),
    speed = document.getElementById('mode'),
    resol_div = document.getElementById('resol'),
    fps_div = document.getElementById('fps');

hidden_url.hidden = true;

img_file.onchange = () => {
    let reader = new FileReader();

    reader.readAsDataURL(img_file.files[0]);

    reader.onload = () => {
        thumbnail.setAttribute('src', reader.result);
    }
}

function getVideo_local() {
    let reader = new FileReader();

    if (video_file.files[0] !== undefined) {
        showProgress();

        link.value = '';
        player.style.display = 'none';
        local_player.style.display = 'block';

        reader.readAsDataURL(video_file.files[0]);

        reader.onload = () => {
            video_source.setAttribute('src', reader.result + '#t=0.1');
            player.setAttribute('src', '/static/asset/thumbnail.png');
            hidden_url.setAttribute('value', '');
            
            resol_div.style.display = 'none';
            fps_div.style.display = 'none';

            setTimeout(() => {
                local_player.load();
                hiddenProgress();
            }, 0);
        }
    } else {
        video_source.setAttribute('src', '');
        local_player.load();
        alert('비디오를 선택해주세요.');
    }
}

function getVideo_youtube() {
    showProgress();
    local_player.style.display = 'none';
    player.style.display = 'block';

    player.setAttribute('src', `https://youtube.com/embed/${splitVideoId(link.value)}`);
    hidden_url.setAttribute('value', `https://youtube.com/embed/${splitVideoId(link.value)}`);
    video_file.value = ''

    resol_div.style.display = 'block';
    fps_div.style.display = 'block';

    hiddenProgress();

    return `https://youtube.com/embed/${splitVideoId(link.value)}`
}

function splitVideoId(link) {
    return link.split('?v=')[1];
}

function setHref_local(base, second) {
    return `${base}#t=${second}`;
}

function setHref_youtube(base, second) {
    return `${base}?autoplay=1&start=${second}`;
}

function getOptions() {
    let result = {
        model: '',
        calc: '',
        fps: 0,
        len: 0,
        resol: '',
        mode: 'normal',
        type: ''
    };

    result.model = model.options[model.selectedIndex].text

    if (speed.checked)
        result.mode = 'speed';
    else
        result.mode = 'normal';

    if (video_file.value !== '') {
        result.type = 'local';
    } else if (player.getAttribute('src').includes('youtube')) {
        result.type = 'youtube';
    } else {
        result.type = 'none';
    }

    Array.from(calc).forEach(item => {
        if (item.checked) {
            result.calc = item.value;
        }
    })

    Array.from(fps).forEach(item => {
        if (item.checked) {
            result.fps = item.value;
        }
    })

    Array.from(len).forEach(item => {
        if (item.checked) {
            result.len = item.value;
        }
    })

    Array.from(resol).forEach(item => {
        if (item.checked) {
            result.resol = item.value;
        }
    })

    return result;
}

function setPredict(src, type) {
    let base = ''

    if (type === 'youtube')
        base = player.getAttribute('src');
    else
        base = video_source.getAttribute('src').split('#t=')[0];

    while (result_ul.hasChildNodes()) {
        result_ul.removeChild(result_ul.firstChild);
    }

    Array.from(src).forEach((item) => {
        const split = item[1].split('/');
        const second = split[split.length - 1].split('.')[0];
        const a = document.createElement('a');
        const li = document.createElement('li');

        li.appendChild(a)
        result_ul.appendChild(li);
        li.addEventListener('click', () => {
            if (type === 'youtube') {
                player.setAttribute('src', setHref_youtube(base, second));
            } else {
                local_player.setAttribute('src', setHref_local(base, second));
                local_player.play();
            }
        });

        a.innerText = convertSecond(second);
    })
}

function convertSecond(second) {
    let min = (parseInt(second / 60)).toString();
    let sec = (second % 60).toString();

    if (min < 10)
        min = '0' + min;

    if (sec < 10)
        sec = '0' + sec;

    return min + ' : ' + sec
}

function showProgress() {
    const modal = document.getElementById('modal');
    modal.style.display = 'block';
}

function hiddenProgress() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

function sendData() {
    const img = document.getElementById('img-file')
    const video = document.getElementById('video-file')
    const data = new FormData()

    const result = getOptions();

    if (result.type !== 'none' && img_file.value !== '') {
        data.append('thumbnail', img.files[0]);
        result.type === 'youtube' ? data.append('url', getVideo_youtube()) : data.append('inputVideo', video.files[0]);
        data.append('model', result.model);
        data.append('calc', result.calc);
        data.append('fps', result.fps);
        data.append('resol', result.resol);
        data.append('len', result.len);
        data.append('mode', result.mode);
        data.append('type', result.type);

        const config = {
            method: 'POST',
            body: data
        }

        showProgress();

        fetch('/api/startAnalyze', config)
            .then((res) => {
                res.json().then((data) => {
                    if (data.success) {
                        if (data.mode === 'cos') {
                            setPredict(data.result_cos, result.type);
                        } else {
                            setPredict(data.result_eucl, result.type);
                        }
                    } else {
                        const msg = data.err === 'none_resol' ? '해당 동영상은 선택하신 해상도를 지원하지 않습니다.' : data.err === 'none_fps' ? '해당 동영상은 선택하신 fps를 지원하지 않습니다.' : '1시간 이상의 동영상은 서비스하지 않습니다.'
                        alert(`에러가 발생했습니다. \n${msg}`)
                    }
                })

                hiddenProgress();
            })
    } else {
        alert('동영상이나 비교 이미지 업로드 상태를 다시 확인해주세요.\n계속해서 에러 발생시 새로고침 후 다시 진행해주세요.')
    }
}