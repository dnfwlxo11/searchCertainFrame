const file = document.getElementById('img-file'),
    player = document.getElementById('player'),
    link = document.getElementById('video-link'),
    hidden_url = document.getElementById('hidden-url'),
    thumbnail = document.getElementById('thumbnail'),
    result_ul_cos = document.getElementById('result-ul-cos'),
    result_ul_eunc = document.getElementById('result-ul-eunc');

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

function sendData() {
    const img = document.getElementById('img-file')

    const data = new FormData()
    data.append('file', img.files[0]);
    data.append('url', getVideo());
    data.append('model', 'InceptionV3');
    data.append('calc', 'cos');
    data.append('fps', 30);
    data.append('resol', '360p');
    data.append('len', 10);

    const config = {
        method: 'POST',
        body: data
    }

    fetch('/api/startAnalyze', config)
        .then((res) => {
            res.json().then((data) => {
                if (data.success) {
                    const base = player.getAttribute('src');
                    const result = document.getElementById('result-div');
                    const cos = data.result_cos;
                    const eunc = data.result_eunc;

                    cos.reverse();

                    while (result_ul_cos.hasChildNodes()) {
                        result_ul_cos.removeChild(result_ul_cos.firstChild);
                    }

                    Array.from(cos).forEach((item) => {
                        const split = item[1].split('/');
                        const second = split[split.length - 1].split('.')[0];
                        const a = document.createElement('a');
                        const li = document.createElement('li');

                        li.appendChild(a)
                        result_ul_cos.appendChild(li);
                        li.addEventListener('click', () => {
                            player.setAttribute('src', setHref(base, second));
                        });

                        a.innerText = second;
                    })

                    // Array.from(eunc).forEach((item) => {
                    //     const split = item[1].split('/')
                    //     const second = split[split.length-1].split('.')[0]
                    //     const a = document.createElement('a')

                    //     result_ul_eunc.appendChild(a);
                    //     a.addEventListener('click', () => {
                    //         if (second !== 0 || second !== (data.len -1)) {
                    //     player.setAttribute('src', setHref(base, second));
                    //     a.innerText = second/3600 + '시간 ' + second%3600/60 + '분 ' + second%3600%60 + '초';
                    // }
                    //     });
                    // })

                    result.appendChild(result_ul_cos);
                    // result.appendChild(result_ul_eunc);
                } else {
                    const msg = data.err === 'none_resol' ? '해당 동영상은 선택하신 해상도를 지원하지 않습니다.' : '해당 동영상은 선택하신 fps를 지원하지 않습니다.'
                    alert(`에러가 발생했습니다. \n${msg}`)
                }
            })
        })
}