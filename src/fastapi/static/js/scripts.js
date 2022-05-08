function checkGif() {
    setTimeout(() => {
        fetch("/checkGIF", {method: "GET"})
        .then((res) => {
            res.json()
            .then((resp) => {
                if ((resp.answ) && (resp.path)) {
                    let div = document.getElementById("gif");
                    let img = document.createElement("img");
                    img.id = "gifImage"
                    img.src = "static/working/" + resp.path;
                    div.style['display'] = 'inherit';
                    div.prepend(img);
                    let pb = document.getElementById('progressBar');
                    pb.value = 100;
                } else {
                    setTimeout(checkGif, 10000);
                }
            })
        })    
    }, 0)
}

function checkProgress() {
    setTimeout(() => {
        fetch("/getProgress", {method: "GET"})
        .then((res) => {
            res.json()
            .then((resp) => {
                if (resp.prg)  {
                    let pb = document.getElementById('progressBar');
                    if (resp.prg >= 100 || pb.value >= 100) {
                        return;
                    }
                    pb.value = resp.prg;
                }
                setTimeout(checkProgress, 1000);
            })
        })    
    }, 0)
}