from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/geojson/{filename}")
def get_geojson(filename: str):
    path = os.path.join("geojson", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type='application/geo+json')
    return {"error": "File not found"}
