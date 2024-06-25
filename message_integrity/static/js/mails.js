const splitted_url = window.location.toString().split("/")
const user_id = parseInt(splitted_url[splitted_url.length-1])

const socket = new WebSocket("ws://127.0.0.1:8000/ws/11")

socket.onopen = function() {
  socket.send(JSON.stringify({user_id: user_id}))
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data)
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
    const progressBar = $("#check-mails-progress-bar")
    const textDiv = $("#check-emails-text")

    textDiv.text(`Checked ${data.checked} of ${data.all}`)
    progressBar.attr("max", data.all)
    progressBar.attr("value", data.checked)
}

function setUploadMode(data){
    const progressBar = $("#upload-mails-progress-bar")
    const textDiv = $("#upload-emails-text")

    textDiv.text(`Uploaded ${data.uploaded} of ${data.all}`)
    progressBar.removeAttr("hidden")
    progressBar.attr("max", data.all)
    progressBar.attr("value", data.uploaded)

    addTableRow(data.data, data.uploaded)
}

function addTableRow(data, mail_number){
    if (!data.mail){
        return
    }
    const node = document.createElement("div")

    let mailFiles = ""
    data.files.forEach((value, index) => {
        mailFiles += `<div>${value}</div>`
    })

    node.className = "row_content"
    node.innerHTML = `
        <div class="mail_number">${mail_number}</div>
        <div class="mail_id">${data.mail.id}</div>
        <div class="mail_uid">${data.mail.uid}</div>
        <div class="mail_subject">${data.mail.subject.substring(0, 100)}</div>
        <div class="mail_text">${data.mail.text.substring(0, 100)}</div>
        <div class="mail_sent_date">${data.mail.sent_date}</div>
        <div class="mail_received_date">${data.mail.received_date}</div>
        <div class="mail_files">${mailFiles}</div>
    `

    const contentTable = $(".content_table")
    contentTable.css("display", "flex")
    contentTable.append(node)
}
