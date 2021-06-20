const file = document.getElementById('img-file'),
    player = document.getElementById('player'),
    link = document.getElementById('video-link'),
    hidden_url = document.getElementById('hidden-url'),
    thumbnail = document.getElementById('thumbnail');

hidden_url.hidden = true;


file.onchange = function () {
    let reader = new FileReader();

    reader.readAsDataURL(file.files[0]);
    console.log(reader.result)
    reader.onload = () => {
        thumbnail.setAttribute('src', reader.result);
    }
}

function getVideo() {
    player.setAttribute('src', `https://youtube.com/embed/${splitVideoId(link.value)}`);
    hidden_url.setAttribute('value', `https://youtube.com/embed/${splitVideoId(link.value)}`)
}

function splitVideoId(link) {
    return link.split('?v=')[1];
}