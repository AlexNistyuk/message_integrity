const splitted_url = window.location.toString().split("/")
const user_id = parseInt(splitted_url[splitted_url.length-1])



const socket = new WebSocket("ws://127.0.0.1:8000/ws/11")

socket.onopen = function() {
  socket.send(JSON.stringify({user_id: user_id}))
};

socket.onmessage = function(event) {
    data = JSON.parse(event.data)
    if (data.mode === "check"){
        setCheckMode(data)
    } else if (data.mode === "upload"){
        setUploadMode(data)
    }

};

socket.onerror = function(error) {
  alert("Ошибка " + error.message);
};


function setCheckMode(data){
    const progressBar = document.getElementById("progress-bar")
    const textDiv = document.getElementById("text")

    textDiv.innerText = `Checked ${data.checked} of ${data.all}`
    progressBar.setAttribute("max", data.all)
    progressBar.setAttribute("value", data.checked)
}

function setUploadMode(data){
    const progressBar = document.getElementById("progress-bar")
    const textDiv = document.getElementById("text")

    textDiv.innerText = `Uploaded ${data.uploaded} of ${data.all}`
    progressBar.setAttribute("max", data.all)
    progressBar.setAttribute("value", data.uploaded)
}
