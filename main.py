from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from security.auth import hash_password, verify_password, create_access_token
import os

load_dotenv()



if "RENDER" in os.environ:
    from backend.routes.api import router  # For Render.com
    from backend.database.db import engine, Base


else:
    from routes.api import router  # For local development
    from database.db import engine, Base

from fastapi import FastAPI




app = FastAPI()

# Register API routes
app.include_router(router)






@app.get("/")
def root():
    return {"message": "IFRS 9 Impairment Tool API is running"}

@app.post("/hey")
def root():
    return {"message": "IFRS 9 Impairment Tool API is running"}




# Create tables
Base.metadata.create_all(bind=engine)

