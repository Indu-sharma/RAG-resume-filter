from fastapi import FastAPI, UploadFile, File
import os
from typing import List
from . rag_pipeline.pipeline import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

engine = None
chat_initializer = None

UPLOAD_DIR = "backend/uploads/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
@app.get("/")
def read_root():
    return RedirectResponse(url="/frontend/index.html")


@app.post("/upload/")
def upload_resumes(files: List[UploadFile] = File(...)):
    global engine
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
    engine = initialise_engine()
    return {"message": "Resumes uploaded successfully and Query Engine is ready!"}

@app.get("/search/")
def search_resumes(query: str):
    document_files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
    if not document_files:
        return {"message": "No resumes available for searching."}
    else:
        print(f"Resumes are found!")
    results = query_response(query, engine, chat_initializer)
    print(f"my results:: {results}")
    return {"results": results}

def initialise_engine():
    global engine
    global chat_initializer
    folder_path = 'backend/uploads/'
    engine = initialize_query_engine(folder_path)
    chat_initializer = initialize_conversation()

if __name__ == "__main__":
    import uvicorn
    initialise_engine()
    uvicorn.run(app, host="127.0.0.1", port=8080)