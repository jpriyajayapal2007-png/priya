from fastapi import FastAPI

app = FastAPI(title="Pocket Smart AI")

@app.get("/")
def root():
    return {"message": "Pocket Smart AI Running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}