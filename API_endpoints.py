from fastapi import FastAPI, UploadFile
from pipelines.pdf_to_topics import pdf_to_topics
from pipelines.topic_to_mindmap import topic_to_mindmap

app = FastAPI()

@app.post("/pdf/topics")
async def get_topics(file: UploadFile):
    path = f"temp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return pdf_to_topics(path)

@app.post("/pdf/mindmap")
async def get_mindmap(file: UploadFile, topic: str):
    path = f"temp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return topic_to_mindmap(path, topic)
