from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title='Creative Generate API',
    description='API for generating creative content', 
    version='1.0.0')


@app.get("/")
def read_root():
    return {"test": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, "0.0.0.0", port=8001, reload=True)

