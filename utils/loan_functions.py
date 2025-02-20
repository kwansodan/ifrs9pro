from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Function to process supported files
def process_file(file: UploadFile):
    # Placeholder for further processing
    return f"File '{file.filename}' has been processed."

# Route to handle file upload
def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided.")

    # Determine the file extension
    _, file_extension = os.path.splitext(file.filename)
    file_extension = file_extension.lower()

    # Check if the file type is supported
    if file_extension not in ['.csv', '.xlsx', '.xls']:
        raise HTTPException(status_code=400, detail=f"File type '{file_extension}' not supported. Only .csv, .xlsx, and .xls are allowed.")

    # Pass to another function for processing
    result = process_file(file)

    return JSONResponse(content={"message": result})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
