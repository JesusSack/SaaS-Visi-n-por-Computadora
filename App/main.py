from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from celery import Celery
import shutil
import os

app = FastAPI(title="Vision SaaS MVP")

# conecta la URL http://localhost:8000/storage con la carpeta interna /storage
app.mount("/storage", StaticFiles(directory="/storage"), name="storage")

celery_app = Celery('tasks', broker='redis://redis:6379/0')

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    upload_folder = "/storage/uploads"
    os.makedirs(upload_folder, exist_ok=True)
    
    file_location = f"{upload_folder}/{file.filename}"
    
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

  
    task = celery_app.send_task('tasks.process_image', args=[file_location])

    return {
        "status": "processing", 
        "original_url": f"/storage/uploads/{file.filename}",
        "task_id": task.id,
        "message": "Procesando. Verifica /debug-files para ver los resultados."
    }

@app.get("/debug-files")
def debug_files():
    path = "/storage/uploads"
    if not os.path.exists(path):
        return {"error": "¡La carpeta /storage/uploads NO existe dentro del contenedor API!"}
    
    try:
        files = os.listdir(path)
        return {
            "ruta_interna": path,
            "total_archivos": len(files),
            "archivos_encontrados": files,
            "instruccion": "Para ver una imagen, copia un nombre de archivo y pegalo al final de: http://localhost:8000/storage/uploads/"
        }
    except Exception as e:
        return {"error": str(e)}