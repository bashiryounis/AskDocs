from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Query

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from src.utils.weavite import weaviate_client , db
from src.utils.helper import save_file

router = APIRouter()

UPLOAD_DIR = "/app/data"


@router.delete("clean_db")
def clean_db(): 
    """
    clean weavite db 
    """
    try:
        weaviate_client.collections.delete_all()
        return "weavite db is cleaned"
    finally : 
        weaviate_client.close()

@router.post("/upload-file/")
def upload_file(
    file: UploadFile = File(..., description="Upload your document here"),
): 
    file_path = save_file(dir=UPLOAD_DIR,file=file)
    print(file_path)
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()
    db.add_documents(documents=docs)
    return file_path