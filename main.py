import sys
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="NPS Saathi API", description="AI-powered Pension Advisory System")

@app.get("/")
def read_root():
    return {"message": "Welcome to NPS Saathi. The API is running."}

if __name__ == "__main__":
    print("Starting NPS Saathi System...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
