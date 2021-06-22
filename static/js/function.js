const file = document.getElementById('img-file'),
    player = document.getElementById('player'),
    link = document.getElementById('video-link'),
    hidden_url = document.getElementById('hidden-url'),
    thumbnail = document.getElementById('thumbnail'),
    result_ul_cos = document.getElementById('result-ul-cos'),
    result_ul_eunc = document.getElementById('result-ul-eunc'),
    model = document.getElementById('model'),
    calc = document.getElementsByName('similar_calc'),
    resol = document.getElementsByName('video_res'),
    fps = document.getElementsByName('video_fps'),
    len = document.getElementsByName('predict_li');

hidden_url.hidden = true;

file.onchange = () => {
    let reader = new FileReader();

    reader.readAsDataURL(file.files[0]);

    reader.onload = () => {
        thumbnail.setAttribute('src', reader.result);
    }
}

function getVideo() {
    player.setAttribute('src', `https://youtube.com/embed/${splitVideoId(link.value)}`);
    hidden_url.setAttribute('value', `https://youtube.com/embed/${splitVideoId(link.value)}`);

    return `https://youtube.com/embed/${splitVideoId(link.value)}`
}

function splitVideoId(link) {
    return link.split('?v=')[1];
}

function move(time) {
    player.setAttribute('src', `https://youtube.com/embed/${splitVideoId(link.value)}?autoplay=1&start=${time}`);
}

function setHref(base, second) {
    return `${base}?autoplay=1&start=${second}`;
}

function getOptions() {
    let result = {
        model: '',
        calc: '',
        fps: 0,
        len: 0,
        resol: ''
    };

    result.model = model.options[model.selectedIndex].text

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

function setPredict(src, dst) {
    const base = player.getAttribute('src');
    const result = document.getElementById('result-div');
    const mode = src;

    while (dst.hasChildNodes()) {
        dst.removeChild(dst.firstChild);
    }

    Array.from(mode).forEach((item) => {
        const split = item[1].split('/');
        const second = split[split.length - 1].split('.')[0];
        const a = document.createElement('a');
        const li = document.createElement('li');

        li.appendChild(a)
        dst.appendChild(li);
        li.addEventListener('click', () => {
            player.setAttribute('src', setHref(base, second));
        });

        a.innerText = second;
    })

    result.appendChild(dst);
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
    const data = new FormData()

    const result = getOptions();

    data.append('file', img.files[0]);
    data.append('url', getVideo());
    data.append('model', result.model);
    data.append('calc', result.calc);
    data.append('fps', result.fps);
    data.append('resol', result.resol);
    data.append('len', result.len);

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
                        setPredict(data.result_cos, result_ul_cos);
                        console.log('cos')
                    } else {
                        setPredict(data.result_eunc, result_ul_eunc);
                        console.log('eunc')
                    }
                } else {
                    const msg = data.err === 'none_resol' ? '해당 동영상은 선택하신 해상도를 지원하지 않습니다.' : data.err === 'none_fps' ? '해당 동영상은 선택하신 fps를 지원하지 않습니다.' : '1시간 이상의 동영상은 서비스하지 않습니다.'
                    alert(`에러가 발생했습니다. \n${msg}`)
                }
            })

            hiddenProgress();
        })
}