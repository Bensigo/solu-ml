from api.index import app
import uvicorn
import os


if __name__ == "__main__":
    port = os.getenv("PORT") or 8000
    uvicorn.run("api.index:app", port=port, reload=True, workers=4)

