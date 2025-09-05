from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from io import BytesIO
from app.minio_client import s3_client, create_bucket

app = FastAPI()

# Define el nombre del bucket
bucket_name = "documents"

# Asegúrate de que el bucket exista
create_bucket(bucket_name)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo a MinIO
    """
    try:
        # Lee el archivo como bytes
        file_bytes = await file.read()

        # Subir el archivo a MinIO usando boto3
        s3_client.put_object(Bucket=bucket_name, Key=file.filename, Body=BytesIO(file_bytes))

        return {"message": f"Archivo {file.filename} subido exitosamente."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    """
    Descarga un archivo desde MinIO
    """
    try:
        # Obtener el archivo desde MinIO usando boto3
        file = s3_client.get_object(Bucket=bucket_name, Key=file_name)

        # Guardar el archivo temporalmente
        temp_file_path = f"temp_{file_name}"
        with open(temp_file_path, "wb") as f:
            f.write(file['Body'].read())

        # Retornar el archivo como respuesta
        return FileResponse(temp_file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except Exception as e:
        return {"error": f"Error al descargar el archivo: {str(e)}"}

