from flask import Blueprint, render_template, request, jsonify, send_file
import uuid, os
from .tasks import executor, TASKS, long_processing

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("upload.html")


@main.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    task_id = str(uuid.uuid4())

    upload_path = f"app/uploads/{task_id}.dat"
    result_path = f"app/static/results/{task_id}.txt"
    plot_path = f"app/static/results/{task_id}.png"

    file.save(upload_path)

    # Запуск фоновой обработки
    future = executor.submit(long_processing, upload_path, result_path, plot_path)
    TASKS[task_id] = {
        "future": future,
        "result_path": result_path,
        "plot_path": plot_path,
    }

    return jsonify({"task_id": task_id})


@main.route("/status/<task_id>")
def status(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404

    future = task["future"]

    if future.done():
        return jsonify({
            "ready": True,
            "download_url": f"/download/{task_id}",
            "plot_url": f"/static/results/{task_id}.png"
        })

    return jsonify({"ready": False})


@main.route("/download/<task_id>")
def download(task_id):
    task = TASKS.get(task_id)
    if not task:
        return "Task not found", 404

    return send_file(task["result_path"], as_attachment=True)
