import shutil
import os 
from fastapi import  UploadFile


def save_file(dir: str, file: UploadFile ):
    """
    Save file in the specified directory.
    """
    os.makedirs(dir, exist_ok=True)
    file_path = os.path.join(dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


