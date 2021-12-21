import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "GAME SERVER root router"


@app.get("/map")
def port():
    return {
        "mapName": "jsonTestMap",
        "mapCode": "ABCDEFG",
        "blocks": [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3]
        ]
    }


uvicorn.run(app, host="0.0.0.0", port=10000)
