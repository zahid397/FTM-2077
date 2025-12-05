from mcp.server.fastapi import FastAPIMessageQueue
import uvicorn
from backend.main import app

if __name__ == "__main__":
    mq = FastAPIMessageQueue(app)
    uvicorn.run(
        mq.app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
