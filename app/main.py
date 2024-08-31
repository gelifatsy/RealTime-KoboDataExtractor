from fastapi import FastAPI
from app.webhook.webhook_endpoint import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)