from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.document_parser import extract_text_from_file
from app.services.query_service import embed_and_store_text

import os
import traceback

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate file type
        filename = file.filename.lower()
        if not (filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".txt")):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Read file contents into memory
        contents = await file.read()

        # Save temporarily for OCR if needed
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Extract text
        extracted_text = extract_text_from_file(temp_path)
        if not extracted_text.strip():
            raise HTTPException(status_code=500, detail="No text extracted from document")

        # Embed & store
        embed_and_store_text(extracted_text, file.filename)


        # Clean up
        os.remove(temp_path)

        return {"message": f"{file.filename} uploaded and processed successfully."}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
