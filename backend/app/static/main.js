const socket = io();
let currentTaskId = null;

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", document.getElementById("fileInput").files[0]);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    currentTaskId = data.task_id;

    document.getElementById("progressCard").classList.remove("hidden");
});

socket.on("progress", (msg) => {
    if (msg.task_id !== currentTaskId) return;
    if (typeof msg.percent !== "number") return; 

    const percent = msg.percent;
    document.getElementById("progressFill").style.width = percent + "%";
    document.getElementById("progressText").textContent = percent + "%";
});

socket.on("finished", (msg) => {
    if (msg.task_id !== currentTaskId) return;

    document.getElementById("progressFill").style.width = "100%";
    document.getElementById("progressText").textContent = "Готово!";

    document.getElementById("downloadLink").href = msg.result_url;
    document.getElementById("resultImage").src = msg.plot_url;
    document.getElementById("resultCard").classList.remove("hidden");
});

// async function loadResult() {
//     console.log('hehe')
//     const r = await fetch(`/result/${currentTaskId}`);
//     const data = await r.json();

//     document.getElementById("downloadLink").href = data.file_url;
//     document.getElementById("resultImage").src = data.plot_url;

//     document.getElementById("resultCard").classList.remove("hidden");
// }
const fileInput = document.getElementById("fileInput");
const fileNameSpan = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileNameSpan.textContent = fileInput.files[0].name;
    } else {
        fileNameSpan.textContent = "Файл не выбран";
    }
});