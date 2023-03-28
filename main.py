from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGION_FILE = os.path.join(BASE_DIR, "kartAI", "training_data", "regions", "small_building_region.json")

@app.post("/update_coordinates")
async def update_coordinates(coordinates: list):
    with open(REGION_FILE, "r") as file:
        data = json.load(file)
    data["coordinates"] = [coordinates]
    with open(REGION_FILE, "w") as file:
        json.dump(data, file)
    return {"status": "success"}
