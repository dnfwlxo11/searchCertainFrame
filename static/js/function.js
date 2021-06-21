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

function sendData() {
    const img = document.getElementById('img-file')

    const data = new FormData()
    data.append('file', img.files[0]);
    data.append('url', getVideo())
    data.tar

    const config = {
        method: 'POST',
        body: data
    }

    fetch('/api/startAnalyze', config)
    .then((res) => {
        res.json().then((data) => {
            const result = document.getElementById('result-div');
            const cos = data.result_cos;
            const eunc = data.result_eunc;
            const path = data.path;

            // Array.from(cos).forEach((item) => {
            //     console.log(item[0], item[1])

            //     const img = document.createElement('img')
            //     const li = document.createElement('li');

            //     img.setAttribute('src', `{{ url_for(filename="${JSON.parse(item[1])}") }}`)
            //     li.setAttribute('class', 'result-cos');
            //     li.appendChild(img);
            //     result_ul_cos.appendChild(li);
            // })

            // Array.from(eunc).forEach((item) => {
            //     const img = document.createElement('img')
            //     const li = document.createElement('li');

            //     img.setAttribute('src', `{{ url_for(filename="${JSON.parse(item[1])}") }}`)
            //     li.setAttribute('class', 'result-eunc');
            //     li.appendChild(img);
            //     result_ul_eunc.appendChild(li);
            // })

            // result.appendChild('ul')
        })
    })
}