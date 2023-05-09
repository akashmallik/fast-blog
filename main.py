from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def index():
    return {
        "data": {
            "status": "success",
            "version": "0.0.1"
        }
    }
