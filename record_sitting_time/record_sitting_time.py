from fastapi import FastAPI, HTTPException
import uvicorn
from datetime import datetime
import json
from bson import ObjectId

from data_service import DataService

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = FastAPI()

data_service = DataService()

@app.get("/")
async def root():
    return "Hello World"

@app.get("/sitting-time")
async def get_sitting_time():
    result = data_service.db_get()
    return json.dumps(result, cls=CustomJSONEncoder)

@app.post("/sitting-time")
async def post_sitting_time(start_time, end_time):
    try:
        doc = {
            "start_time": datetime.fromisoformat(start_time),
            "end_time": datetime.fromisoformat(end_time)
        }
        data_service.db_post(doc)
        return
    except:
        raise HTTPException(status_code=404, detail="Wrong Input Type")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

