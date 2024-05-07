from app.api.index import app
import uvicorn
import os


if __name__ == "__main__":
    port = os.getenv("PORT") or 8000
    uvicorn.run("app.api.index:app", port=port, reload=True, workers=4, host="0.0.0.0")

