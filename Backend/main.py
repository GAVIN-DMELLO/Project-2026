from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api import gemini_call

app = FastAPI()

class SummaryRequest(BaseModel):
  youtubeurl : str

origins = [
  "http://localhost:5173/summarise",
  "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/summarise")
async def handle_summary(request : SummaryRequest):
  summary_text = gemini_call(request.youtubeurl)
  return {"summary":summary_text}