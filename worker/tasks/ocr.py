from worker.worker import app


@app.task
def ocr_task(file_path: str):
    return f"Processed: {file_path}"
