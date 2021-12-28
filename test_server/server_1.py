import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "AI SERVER root router"


@app.get("/ai")
def ai():
    print("인공지능 처리를 하는 중입니다.")

    # out = model(x)

    out = "cat"
    return out


uvicorn.run(app, host="0.0.0.0", port=8000)
